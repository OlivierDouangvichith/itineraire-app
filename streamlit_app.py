import altair as alt
import numpy as np
import pandas as pd
import streamlit as st
from typing import List, Tuple
from st_combobox import st_combobox
import wikipedia

"""
# Welcome to the Project Itinerary !
"""


# function with list of labels
def search_wikipedia(searchterm: str) -> List[any]:
    return wikipedia.search(searchterm) if searchterm else []

# pass search function to combobox
selected_value = st_combobox(
    search_wikipedia,
    label="Titre 1",
    key="wiki_combobox",
)

# pass search function to combobox
selected_value2 = st_combobox(
    search_wikipedia,
    label="Titre 2",
    key="wiki_combobox2",
)

