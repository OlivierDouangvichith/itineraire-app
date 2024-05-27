# Core Pkgs
import streamlit as st
st.set_page_config(page_title="Itinerary Web App", page_icon="👍", layout="centered", initial_sidebar_state="auto")

import psycopg2

def filter_pois(position, pois, radius_km):
    filtered_pois = []
    for poi in pois:
        poi_latitude, poi_longitude = float(poi[1]), float(poi[2])
        if -90 <= poi_latitude <= 90:
            poi_position = (poi_latitude, poi_longitude)
            if geodesic(position, poi_position).kilometers <= radius_km:
                filtered_pois.append(poi)
        else:
            print(f"Latitude out of range for POI {poi}")
    return filtered_pois

def create_graph(tx, filtered_pois, clusters, clustered_points):
    existing_clusters = set(tx.run("MATCH (c:Cluster) RETURN c.name").value())
    
    for i in range(len(final_clusters)):
        cluster_name = f"Cluster_{i}"
        if cluster_name not in existing_clusters:
            tx.run("CREATE (c:Cluster {name: $name})", name=cluster_name)

    for i, point in enumerate(clustered_points):
        latitude, longitude = point
        cluster_name = f"Cluster_{clusters[i]}"
        tx.run(
            "CREATE (poi:POI {latitude: $latitude, longitude: $longitude})",
            latitude=latitude, longitude=longitude
        )
        tx.run(
            "MATCH (poi:POI {latitude: $latitude, longitude: $longitude}), (cluster:Cluster {name: $cluster_name}) "
            "CREATE (poi)-[:BELONGS_TO]->(cluster)",
            latitude=latitude, longitude=longitude, cluster_name=cluster_name
        )

def main():
    """Itinerary web app avec Streamlit"""

    title_template = """
    <div style="background-color:blue; padding:8px;">
    <h1 style="color:cyan">Itinerary Web App</h1>
    </div>
    """

    st.markdown(title_template, unsafe_allow_html=True)

    subheader_template = """
    <div style="background-color:cyan; padding:8px;">
    <h3 style="color:blue">Powered by Streamlit</h1>
    </div>
    """

    st.markdown(subheader_template, unsafe_allow_html=True)
    st.sidebar.image("france_tourisme.jpg", use_column_width=True)

    activity = ["Menu 1", "Menu 2", "Menu 3", "About"]
    choice = st.sidebar.selectbox("Menu", activity)

    if choice == "Menu 1":
        st.subheader("Menu 1 TEST")
        st.write("")

        main_activity = ["CulturalSite", "ParkAndGarden", "PlaceOfInterest", "PointOfInterest"]
        main_choice = st.selectbox("Category", main_activity)

        db_params = {
            'host': st.secrets["DB_HOST"],
            'port': st.secrets["DB_PORT"],
            'database': st.secrets["DB_NAME"],
            'user': st.secrets["DB_USER"],
            'password': st.secrets["DB_PWD"]
        }

        conn = psycopg2.connect(**db_params)
        cursor = conn.cursor()

        # Liste des mots spécifiés
        mots = ["Culture", "Religion", "Sport", "Loisir", "Divertissement", "Hebergement", "Restauration", 
                "Boisson", "Banque", "Hebergement", "Autre", "Plage", "Mobilité réduite", "Moyen de locomotion", 
                "Montagne", "Antiquité", "Histoire", "Musée", "Détente", "Bar", "Commerce local", "Point de vue", 
                "Nature", "Camping", "cours deau", "Service", "Monument", "Jeunesse", "Apprentissage", "Marché", 
                "Vélo", "Magasin", "Animaux", "Location", "Parcours", "Santé", "Information", "Militaire", "Parking", 
                "Marche à pied", "POI", "Piscine"]

        # Créer des cases à cocher pour chaque mot
        mots_selectionnes = []
        for mot in mots:
            mots_selectionnes.append(st.checkbox(mot))

        # Convertir les mots sélectionnés en une liste
        mots_coche_liste = [mots[i] for i in range(len(mots)) if mots_selectionnes[i]]

        # Requête pour sélectionner les POI en fonction des types cochés
        if mots_coche_liste:
            cursor.execute("SELECT dt.label_fr, dt.latitude, dt.longitude, tp.type FROM datatourisme dt JOIN liaison_datatourisme_types_de_poi ldtp ON dt.id = ldtp.id_datatourisme JOIN types_de_poi tp ON ldtp.id_type_de_poi = tp.id WHERE tp.type IN %s GROUP BY dt.label_fr, dt.latitude, dt.longitude, tp.type", (tuple(mots_coche_liste),))
        else:
            cursor.execute("SELECT dt.label_fr, dt.latitude, dt.longitude, tp.type FROM datatourisme dt JOIN liaison_datatourisme_types_de_poi ldtp ON dt.id = ldtp.id_datatourisme JOIN types_de_poi tp ON ldtp.id_type_de_poi = tp.id GROUP BY dt.label_fr, dt.latitude, dt.longitude, tp.type")

        rows = cursor.fetchall()
        conn.commit()

        # Position choisie pour le test
        reference_position = (48.2115397, 6.7204365)

        # POIs dans un rayon de 50 km autour de la position
        filtered_pois = filter_pois(reference_position, rows, 50)

        # Création de la matrice de caractéristiques pour l'algorithme K-Means
        X = [(row[1], row[2]) for row in filtered_pois]

        # Application de K-Means pour regrouper les points d'intérêt (POI) en clusters
        max_clusters = min(10, len(filtered_pois))
        kmeans = KMeans(n_clusters=max_clusters, n_init=10)
        kmeans.fit(X)
        centroids = kmeans.cluster_centers_
        clusters = kmeans.labels_

        # Assignation des points aux clusters en limitant à un maximum de 10 points par cluster
        cluster_points = defaultdict(list)
        for i, point in enumerate(X):
            cluster_index = clusters[i]
            cluster_points[cluster_index].append(point)

        # Réduire le nombre de points par cluster à un maximum de 10
        final_clusters = []
        for cluster_index, points in cluster_points.items():
            if len(points) <= 10:
                final_clusters.append(points)
            else:
                # Si le cluster contient plus de 10 points, sélectionner les 10 points les plus proches du centroïde
                centroid = centroids[cluster_index]
                distances = [geodesic(centroid, point).kilometers for point in points]
                closest_points_indices = np.argsort(distances)[:10]
                final_clusters.append([points[i] for i in closest_points_indices])

        # Convertir les clusters en une liste plate
        clustered_points = [point for sublist in final_clusters for point in sublist]

        # Connexion à la base de données Neo4j
        uri = "bolt://127.0.0.1:7687"
        username = "neo4j"
        password = "neo4j"
        driver = GraphDatabase.driver(uri, auth=(username, password))

        # Fonction pour créer le graphe dans Neo4j
        def create_graph(tx):
            # Vérifier l'existence des nœuds Cluster
            existing_clusters = set(tx.run("MATCH (c:Cluster) RETURN c.name").value())
            
            # Création des clusters
            for i in range(len(final_clusters)):
                cluster_name = f"Cluster_{i}"
                if cluster_name not in existing_clusters:
                    tx.run("CREATE (c:Cluster {name: $name})", name=cluster_name)

            # Création des points d'intérêt (POI) et des relations avec les clusters
            for i, point in enumerate(clustered_points):
                latitude, longitude = point
                cluster_name = f"Cluster_{clusters[i]}"
                tx.run(
                    "CREATE (poi:POI {latitude: $latitude, longitude: $longitude})",
                    latitude=latitude, longitude=longitude
                )
                tx.run(
                    "MATCH (poi:POI {latitude: $latitude, longitude: $longitude}), (cluster:Cluster {name: $cluster_name}) "
                    "CREATE (poi)-[:BELONGS_TO]->(cluster)",
                    latitude=latitude, longitude=longitude, cluster_name=cluster_name
                )

        # Création de la session Neo4j et exécution de la transaction
        with driver.session() as session:
            session.write_transaction(create_graph)

        cursor.close()
        conn.close()


    if choice == "Menu 2":
        st.subheader("Menu 2")
        st.write("")

    if choice == "Menu 3":
        st.subheader("Menu 3")
        st.write("")

    if choice == "About":
        st.subheader("About")
        st.write("")

        st.markdown("""
        ### Itinerary Web App made with Streamlit

        for info:
        - [streamlit](https://streamlit.io)
        """)
        

if __name__ == "__main__":
    main()
