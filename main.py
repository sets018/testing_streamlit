import streamlit as st
# Networkx para grafos
import networkx as nx
import sys
# Pandas
import pandas as pd

# Mostrar imágenes
from IPython.display import HTML

# Mathplotlib
import matplotlib.pyplot as plt

st.set_page_config(page_title="Lab 2", layout="wide")

st.title(' Laboratorio 2 - Estructura de datos 2')

# A dictionary of apps in the format of {"App title": "App icon"}
# More icons can be found here: https://icons.getbootstrap.com
#Funcion para mostrar el camino

origin = 'aaaaaa'
destination = 'bbbbbbb'
st.write("origen: "+ origin + "Destino: "+ destination)
