# Core Pkgs
import streamlit as st
st.set_page_config(page_title="Itinerary Web App", page_icon="👍", layout="centered", initial_sidebar_state="auto")

from datetime import datetime, timedelta
import altair as alt
import numpy as np
import pandas as pd
import streamlit as st
from typing import List, Tuple
from st_combobox import st_combobox
import wikipedia
import psycopg2


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

  activity = ["Planification de Voyage", "Méthodologie", "Analyse des données", "A propos"]
  choice = st.sidebar.selectbox("Menu", activity)

  if choice == "Planification de Voyage":
      st.subheader("Configurateur de votre prochain de Voyage")
      st.write("")

      depart_lieu = ["Paris", "Lyon", "Toulouse", "Marseille"]
      depart_choice = st.selectbox("Départ", depart_lieu)

      arrivee_lieu = ["Paris", "Lyon", "Toulouse", "Marseille"]
      arrivee_choice = st.selectbox("Arrivée", arrivee_lieu)

      today = datetime.now()
      tomorrow = today + timedelta(days=1)
      # st.write("tomorrow: ", tomorrow)
      arrivee_date = st.date_input("Date Arrivée", value=None, min_value=tomorrow, format="DD/MM/YYYY")

      duree_jour = st.number_input("Durée de visite", min_value=1, max_value=None, value="min", placeholder="En jour...")


      # Paramètres de la base de données
      db_params = {
          'host': st.secrets["DB_HOST"],
          'port': st.secrets["DB_PORT"],
          'database': st.secrets["DB_NAME"],
          'user': st.secrets["DB_USER"],
          'password': st.secrets["DB_PWD"]
      }

      # Connexion à la base de données
      conn = psycopg2.connect(**db_params)
      cur = conn.cursor()

      # Requête pour sélectionner les 10 premières lignes de la table datatourisme
      cur.execute("SELECT id, type FROM datatourisme10 LIMIT 10")

      # Récupération des résultats
      rows = cur.fetchall()

      # Parcours des résultats
      for row in rows:
          id_datatourisme, types = row

          st.write("//////////////////////////////////////////////////////////")
          st.write("id_datatourisme: ", id_datatourisme)
          st.write("types: ", types)

          # Séparation des types par des virgules
          types_list = [t.strip() for t in types.split(',')]

          st.write("types_list: ", types_list)

          # Vérification pour chaque type
          for t in types_list:
              # Recherche du type dans la table types_de_poi
              cur.execute("SELECT id, classe FROM types_de_poi WHERE classe = %s", (t,))
              result = cur.fetchone()

              # Si le type est trouvé
              if result:
                  id_type_de_poi, classe = result

                  st.write("----------------")
                  st.write("id_datatourisme: ", id_datatourisme)
                  st.write("id_type_de_poi: ", id_type_de_poi)
                  st.write("classe: ", classe)
                  st.write("----------------")

                  # Insertion dans la table de liaison many-to-many
                  # cur.execute(
                  #    "INSERT INTO liaison_datatourisme_types_de_poi (id_datatourisme, id_type_de_poi) VALUES (%s, %s)",
                  #    (id_datatourisme, id_type_de_poi))

          st.write("//////////////////////////////////////////////////////////")





      # Commit des modifications et fermeture de la connexion
      conn.commit()
      conn.close()

  if choice == "Méthodologie":
      st.subheader("Menu Méthodologie")
      st.write("")

  if choice == "Analyse des données":
      st.subheader("Analyse des données 3")
      st.write("")

  if choice == "A propos":
    st.subheader("A propos")
    st.write("")

    st.markdown("""
    ### Itinerary Web App made with Streamlit

    for info:
    - [streamlit](https://streamlit.io)
    """)




if __name__ == "__main__":
  main()

