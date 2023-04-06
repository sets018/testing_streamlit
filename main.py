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

def show_path(path):
    #Variables contadoras para mostrar precio del vuelo y la duracion
    total_price = 0
    total_duration = 0
    #Iteramos de acuerdo a lo largo que sea el camino
    for i in range(len(path)-1):
        origin = path[i]
        destination = path[i+1]
        duration = DG[origin][destination]["duration"]
        price = DG[origin][destination]["price"]
        
        total_price = total_price+price
        total_duration = total_duration+duration
        st.write("    " + Aeropuertos.loc[origin]["name"] + " -> " + Aeropuertos.loc[destination]["name"])
        st.write("    - Duration: " + str(duration) + " Price: " + str(price) + " $")  
    st.write("\n     Total Duration: " + str(total_duration) + " Total price: " + str(total_price) + " $ \n")
   
#Encuentra todos los caminos mas cortos
def get_all_shortest_paths(DiGraph, origin, destination):
    st.write("*** All shortest paths - Origen: " + origin + " Destino: " + destination)
    for weight in [None, "duration", "price"]:
        st.write("* Ordenando por: " + weight)
        paths = list(nx.all_shortest_paths(DiGraph,
                                          source=origin,
                                          target=destination,
                                          weight=weight))
        for path in paths:
            st.write("   Camino óptimo: " + path)
            show_path(path)
            
def get_shortest_path(DiGraph, origin, destination):
    st.write("*** Origen: " + origin + " Destino: " + destination)
    
    for weight in [None, "duration", "price"]:
        st.write(" Ordenado por: " + weight)
        path = list(nx.astar_path(DiGraph,
                                  (origin),
                                  (destination),
                                  weight=weight
                                 ))
        print("   Camino óptimo: " + path + " ")
        show_path(path)
        
@st.cache_data()        
def load_data(sw):
  #Abriendo el archivo donde tenemos el dataset de los aeropuertos
  Aeropuertos = pd.read_csv('https://raw.githubusercontent.com/lsolaez/Laboratorio-2/main/Aeropuertos.csv')
  #Haciendo que el indice sea la columna code
  Aeropuertos.set_index(["code"], inplace=True)
  #Obteniendo el dataframe de vuelos
  vuelos = pd.read_csv("https://raw.githubusercontent.com/lsolaez/Laboratorio-2/main/vuelos.csv")
  a = Aeropuertos.reset_index()
  code_list = a["code"]
  code_list = code_list.to_list()
  #Creando un grafo dirigido
  DG=nx.DiGraph()
  for row in vuelos.iterrows():
      DG.add_edge(row[1]["origin"],
                  row[1]["destination"],
                  duration=row[1]["duration"],
                  price=row[1]["price"])
      
st.title(' Laboratorio 2 - Estructura de datos 2')

load_data(1)

opcion = st.radio(
    'Seleccione una opcion',
    ("1. Buscar aeropuerto", "2. Buscar vuelo", "3. DFS", "4. BFS")) 

if opcion == "1. Buscar aeropuerto":
        code = st.selectbox('Ingrese el código IATA del aeropuerto a buscar: ',
                            code_list)
        print(Aeropuertos.loc[code])
      
elif opcion == "2. Buscar vuelo":
        origen = st.selectbox("Ingrese el origen del vuelo en código IATA: ",
                             code_list)
    
        if origen not in DG.nodes:
            st.write("El origen no se encuentra en el grafo. Inténtelo de nuevo.")

        destino = st.selectbox("Ingrese el destino del vuelo en código IATA: ",
                             code_list)
        if destino not in DG.nodes:
            st.write("El destino no se encuentra en el grafo. Inténtelo de nuevo.")
            
elif opcion == "3. DFS":
        origen = st.selectbox("Ingrese el nodo origen para el DFS: ",
                             code_list)
        try:
          dfs_nodes = list(nx.dfs_preorder_nodes(DG, source=origen))
          # Imprime los nodos visitados en el recorrido DFS
          for node in dfs_nodes:
              st.write(Aeropuertos.loc[node])
        except KeyError:
            st.write("El nodo ingresado no se encuentra en el grafo.")
elif opcion == "4. BFS":
        origen=input('Ingrese el nodo origen para el BFS: ')
        try:
          bfs_nodes = list(nx.bfs_tree(DG, source=origen))
          # Imprime los nodos visitados en el recorrido DFS
          for node in bfs_nodes:
              st.write(Aeropuertos.loc[node])
        except KeyError:
            st.write("El nodo ingresado no se encuentra en el grafo.")
