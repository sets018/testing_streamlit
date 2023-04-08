import streamlit as st
# Networkx para grafos
import networkx as nx
import sys
import folium
# Pandas

from streamlit_folium import st_folium

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
        if (weight != None):
            st.write("* Ordenando por: " + weight)
        else: 
            st.write("* Ordenando por: None")
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
        if (weight != None):
            st.write(" Ordenado por: " + weight)
        else:
            st.write("Ordenado por: None")
        path = list(nx.astar_path(DiGraph,
                                  (origin),
                                  (destination),
                                  weight=weight
                                 ))
        st.write("camino optimo: " + ", ".join(str(x) for x in path))
        show_path(path)
        plot_shortest_path(path)
 
def plot_shortest_path(path):
    st.write(type(path))
    short_path=nx.DiGraph()
    for i in range(len(path)-1):
        short_path.add_edge(path[i], path[i+1])
    st.write(type(short_path))
    st.write(short_path)
    
def get_vuelos(cities_airports, vuelos): 
    lines_points = []
    for line in vuelos:
        cities = line.split("-")
        for city_code in cities:
            city_coords = (float(cities_airports[cities_airports["Aeropuerto"] == city_code]["Latitud"]),float(cities_airports[cities_airports["Aeropuerto"] == city_code]["Longitud"]))
            lines_points.append(city_coords)
    return lines_points
            
def create_map(cities_airports, lines_points): 
    # Creates map object
    map = folium.Map(location=[5,-86], tiles="OpenStreetMap", zoom_start=3)
    for city in range(0, cities_airports.shape[0]):
        folium.Marker(location=[cities_airports.iloc[city]['Latitud'], cities_airports.iloc[city]['Longitud']],popup = "-Ciudad : " + cities_airports.iloc[city]["localizate"] + "\n"  + "-Codigo: " + cities_airports.iloc[city]['Aeropuerto']).add_to(map)
        lines = folium.PolyLine(lines_points).add_to(map)
    return map
            
#Abriendo el archivo donde tenemos el dataset de los aeropuertos
Aeropuertos = pd.read_csv('https://raw.githubusercontent.com/lsolaez/Laboratorio-2/main/Aeropuertos.csv')
#Haciendo que el indice sea la columna code
Aeropuertos.set_index(["code"], inplace=True)
aeropuertos_code = Aeropuertos.reset_index()
#Obteniendo el dataframe de vuelos
Vuelos = pd.read_csv("https://raw.githubusercontent.com/lsolaez/Laboratorio-2/main/vuelos.csv")
Coordenadas = pd.read_csv("https://raw.githubusercontent.com/lsolaez/Laboratorio-2/main/Coordenadas.csv")
cities_airports = pd.merge(aeropuertos_code, Coordenadas, how='inner', left_on = 'code', right_on = 'Aeropuerto')
code_list = aeropuertos_code["code"]
code_list = code_list.to_list()

#Creando un grafo dirigido
DG=nx.DiGraph()
for row in Vuelos.iterrows():
    DG.add_edge(row[1]["origin"],
    row[1]["destination"],
    duration=row[1]["duration"],
    price=row[1]["price"])
      
st.title(' Laboratorio 2 - Estructura de datos 2')

if st.checkbox('Mostrar grafo de aeropuertos y vuelos'):
    vuelos = Vuelos["origin"] + '-' + Vuelos["destination"]
    vuelos = vuelos.unique()
    
    map = create_map(cities_airports, get_vuelos(cities_airports, vuelos))
    map_fig = st_folium(map, width=725)
    
opcion = st.radio(
    'Seleccione una opcion',
    ("1. Buscar aeropuerto", "2. Buscar vuelo", "3. DFS", "4. BFS")) 

if opcion == "1. Buscar aeropuerto":
        code = st.selectbox('Ingrese el código IATA del aeropuerto a buscar: ',
                            code_list)
        if st.checkbox('get-results for 1. Buscar aeropuerto'):
            map_2 = folium.Map(location=[5,-86], tiles="OpenStreetMap", zoom_start=3)
            airport_query = cities_airports[cities_airports["Aeropuerto"] == code]
            folium.Marker(location=[airport_query["Latitud"].iloc[0], airport_query["Longitud"].iloc[0]],popup = "-Ciudad : " + airport_query["localizate"].iloc[0]  + "\n"  + "-Codigo: " + airport_query["Aeropuerto"].iloc[0]).add_to(map_2)
            map_fig_2 = st_folium(map_2, width=725)
                  
elif opcion == "2. Buscar vuelo":
        origen = st.selectbox("Ingrese el origen del vuelo en código IATA: ",
                             code_list)
        
        if origen not in DG.nodes:
                st.write("El origen no se encuentra en el grafo. Inténtelo de nuevo.")

        destino = st.selectbox("Ingrese el destino del vuelo en código IATA: ",
                                 code_list)
        if destino not in DG.nodes:
                st.write("El destino no se encuentra en el grafo. Inténtelo de nuevo.")
                
        if st.button('get-results'):
            try:
                get_shortest_path(DG, origen, destino)
            except nx.exception.NetworkXNoPath:
                print("No existe un camino entre los nodos de origen y destino.")
                
                
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
       origen = st.selectbox("Ingrese el nodo origen para el BFS: ",
                             code_list)
       try:
          bfs_nodes = list(nx.bfs_tree(DG, source=origen))
          # Imprime los nodos visitados en el recorrido DFS
          for node in bfs_nodes:
              st.write(Aeropuertos.loc[node])
       except KeyError:
            st.write("El nodo ingresado no se encuentra en el grafo.")
