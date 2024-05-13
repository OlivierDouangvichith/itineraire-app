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
      st.subheader("Menu 1")
      st.write("")


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

