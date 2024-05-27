import streamlit as st
import requests

# Titre de l'application
st.title('Clustering des Points d\'intérêt')

# Formulaire pour saisir les paramètres
latitude = st.number_input('Latitude du point de référence', value=44.75)
longitude = st.number_input('Longitude du point de référence', value=4.85)
poi_types = st.text_input('Types d\'activité (séparés par des virgules)', value='Monument')

# Bouton pour exécuter le script
if st.button('Exécuter le script'):
    # URL de votre script CGI
    cgi_url = 'http://99.81.159.66/execute_script.cgi'
    # Paramètres à envoyer dans la requête HTTP
    params = {
        'latitude': latitude,
        'longitude': longitude,
        'poi_types': poi_types
    }
    # Envoyer la requête HTTP GET au script CGI
    response = requests.get(cgi_url, params=params)
    
    # Vérifier si la requête a réussi
    if response.status_code == 200:
        # Afficher la sortie du script CGI
        st.text(response.text)
    else:
        st.error(f'Erreur lors de l\'exécution du script : {response.text}')
