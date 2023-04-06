import streamlit as st
st.set_page_config(page_title="Lab 2", layout="wide")

st.title(' Laboratorio 2 - Estructura de datos 2')

# A dictionary of apps in the format of {"App title": "App icon"}
# More icons can be found here: https://icons.getbootstrap.com
#Funcion para mostrar el camino
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
        print("    %s -> %s\n    - Duration: %s Price: %s $" % (
            Aeropuertos.loc[origin]["name"],
            Aeropuertos.loc[destination]["name"],
            duration, price)
        )
    
    print("\n     Total Duration: %s Total price: %s $ \n" % (
            total_duration, total_price)
    )
#Encuentra todos los caminos mas cortos
def get_all_shortest_paths(DiGraph, origin, destination):
    print("*** All shortest paths - Origen: %s Destino: %s" % (
        origin, destination
    ))
    for weight in [None, "duration", "price"]:
        print("* Ordenando por: %s" % weight)
        paths = list(nx.all_shortest_paths(DiGraph,
                                          source=origin,
                                          target=destination,
                                          weight=weight))
        for path in paths:
            print("   Camino óptimo: %s" % path)
            show_path(path)
    
#Encuentra todos los caminos mas cortos
def get_all_shortest_paths(DiGraph, origin, destination):
    print("*** All shortest paths - Origen: %s Destino: %s" % (
        origin, destination
    ))
    for weight in [None, "duration", "price"]:
        print("* Ordenando por: %s" % weight)
        paths = list(nx.all_shortest_paths(DiGraph,
                                          source=origin,
                                          target=destination,
                                          weight=weight))
        for path in paths:
            print("   Camino óptimo: %s" % path)
            show_path(path)
#Dibuja el camino sobre el grafo
def plot_shortest_path(path):
    print(path)
    positions = nx.circular_layout(DG)
    
    nx.draw(DG, pos=positions,
                node_color='lightblue',
                edge_color='gray',
                font_size=24,
                width=1, with_labels=True, node_size=3500, alpha=0.8
           )
    
    short_path=nx.DiGraph()
    for i in range(len(path)-1):
        short_path.add_edge(path[i], path[i+1])
    
    nx.draw(short_path, pos=positions,
                node_color='dodgerblue',
                edge_color='dodgerblue',
                font_size=24,
                width=3, with_labels=True, node_size=3000
           )
    plt.show()
        
def get_shortest_path(DiGraph, origin, destination):
    print("*** Origen: %s Destino: %s" % (origin, destination))
    
    for weight in [None, "duration", "price"]:
        print(" Ordenado por: %s" % weight)
        path = list(nx.astar_path(DiGraph,
                                  (origin),
                                  (destination),
                                  weight=weight
                                 ))
        print("   Camino óptimo: %s " % path)
        show_path(path)
        plot_shortest_path(path)

 
#Abriendo el archivo donde tenemos el dataset de los aeropuertos
Aeropuertos = pd.read_csv('https://raw.githubusercontent.com/lsolaez/Laboratorio-2/main/Aeropuertos.csv')
#Haciendo que el indice sea la columna code
Aeropuertos.set_index(["code"], inplace=True)
#Obteniendo el dataframe de vuelos
vuelos = pd.read_csv("https://raw.githubusercontent.com/lsolaez/Laboratorio-2/main/vuelos.csv")
#Creando un grafo dirigido
DG=nx.DiGraph()

menu_option =  st.selectbox("Seleccione una opcion",
                           ("1. Buscar aeropuerto","2. Buscar vuelo","3. DFS","4. BFS","5. Salir"))
if (menu_option == "1. Buscar aeropuerto"):
  code = st.text_input('Ingrese el código IATA del aeropuerto a buscar: ')
  st.write(Aeropuertos.loc[code])
elif (menu_option == "2"):
  origen = st.text_input("Ingrese el origen del vuelo en código IATA: ")
  if origen not in DG.nodes:
    st.write("El origen no se encuentra en el grafo. Inténtelo de nuevo.")
   
  destino = st.text_input("Ingrese el destino del vuelo en código IATA: ")
  if destino not in DG.nodes:
    st.write("El destino no se encuentra en el grafo. Inténtelo de nuevo.")
    
  try:
      get_shortest_path(DG, origen, destino)
  except nx.exception.NetworkXNoPath:
      st.write("No existe un camino entre los nodos de origen y destino.")
elif (opcion == "3"):
    origen = st.text_input('Ingrese el nodo origen para el DFS: ')
    try:
      dfs_nodes = list(nx.dfs_preorder_nodes(DG, source=origen))
      # Imprime los nodos visitados en el recorrido DFS
      for node in dfs_nodes:
        st.write(Aeropuertos.loc[node])
    except KeyError:
      st.write("El nodo ingresado no se encuentra en el grafo.")
elif (opcion == "4"):
        origen=text_input('Ingrese el nodo origen para el DFS: ')
        try:
          bfs_nodes = list(nx.bfs_tree(DG, source=origen))
          # Imprime los nodos visitados en el recorrido DFS
          for node in bfs_nodes:
              st.write(Aeropuertos.loc[node])
        except KeyError:
            st.write("El nodo ingresado no se encuentra en el grafo.")
elif (opcion == "5"):
  st.write("¡Hasta luego!")
