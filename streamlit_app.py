# Core Pkgs
import streamlit as st
st.set_page_config(page_title="Itinerary Web App", page_icon="👍", layout="centered", initial_sidebar_state="auto")

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

  activity = ["Menu 1", "Menu 2", "Menu 3", "About"]
  choice = st.sidebar.selectbox("Menu", activity)

  if choice == "Menu 1":
      st.subheader("Menu 1 TEST")
      st.write("")

      # Paramètres de la base de données
      db_params = {
          'host': '188.166.105.53',
          'port': 65001,
          'database': 'postgres',
          'user': 'postgres',
          'password': 'LearnPostgreSQL'
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

