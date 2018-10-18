import urllib.request, json 
import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd
from itertools import combinations

import warnings
warnings.filterwarnings('ignore')

G = nx.Graph()

def usuarios():	
    #url1='https://api.github.com/search/users?q=+type:user+location:colombia'
    url1='https://api.github.com/search/users?q=+type:user+location:colombia+repos:>100+language:java&per_page=100'
    with urllib.request.urlopen(url1) as url:
        users= json.loads(url.read().decode())    
    for item in users['items']:
        del item['id']
        del item['node_id']
        del item['avatar_url']
        del item['gravatar_id']
        del item['url']
        del item['html_url']
        #del item['followers_url']
        del item['following_url']
        del item['gists_url']
        del item['starred_url']
        del item['subscriptions_url']
        del item['organizations_url']
        del item['events_url']
        del item['received_events_url']
        del item['type']
        del item['site_admin']
        del item['score']
        del item['repos_url']            
	#return str(users['items'])
    return users['items']

def seguidores(G, l_usu):
    try:
        for u in l_usu:
            url_seg=u['followers_url'] 
            try:       
                with urllib.request.urlopen(url_seg) as url:
                    seguid= json.loads(url.read().decode())
            except Exception as inst:   
                print("#####función seguidores()######")             
                print("error de conexión")
                print(inst)
                print("##############################")
                return "false"               
            for item in seguid:
                #del item['login']
                del item['id']
                del item['node_id']	
                del item['avatar_url']
                del item['gravatar_id']
                del item['url']
                del item['html_url']
                del item['followers_url']
                del item['following_url']
                del item['gists_url']
                del item['starred_url']
                del item['subscriptions_url']
                del item['organizations_url']
                del item['repos_url']
                del item['events_url']
                del item['received_events_url']
                del item['type']
                del item['site_admin']		
            for s in seguid:
                G.add_edge(u['login'],s['login'])
            return "true"        
    except ValueError:
        print ("error en la conexión")
        return "false" 	

# métricas de Nodos
# density of a graph
def nodeMeasure_density(G): 
    G = nx.convert_node_labels_to_integers(G,first_label=1)
    density = nx.density(G)
    return density

# métricas de Nodos
# degree: número de nodos adyacentes
def nodeMeasure_degree(G):
    #print("G = ")
    #print(nx.degree(G).values())
    #Gtemp = nx.convert_node_labels_to_integers(G,first_label=1)
    #degree_sequence=sorted(nx.degree(Gtemp).values(),reverse=True)     
    degrees = [val for (G, val) in G.degree()]
    dmax=max(degrees) 
    dmin =min(degrees)

    print("############## degrees #############")    
    print(degrees)
    print("####################################")
    print("################ dmax ##############")
    print(dmax)
    print("##############################")
    print("############# dmin #################")
    print(dmin)
    print("####################################")

#maximal-cliques in a graph
def max_cliques(G):    
    #print(list(nx.find_cliques(G)))
    return nx.find_cliques(G)

# Define get_nodes_and_nbrs()
def get_nodes_and_nbrs(G, nodes_of_interest):
    """
    Returns a subgraph of the graph `G` with only the `nodes_of_interest` and their neighbors.
    """
    nodes_to_draw = []
    
    # Iterate over the nodes of interest
    for n in nodes_of_interest:
    
        # Append the nodes of interest to nodes_to_draw
        nodes_to_draw.append(n)
        
        # Iterate over all the neighbors of node n
        for nbr in G.neighbors(n):
        
            # Append the neighbors of n to nodes_to_draw
            nodes_to_draw.append(nbr)
            
    return G.subgraph(nodes_to_draw)

# Define is_in_triangle() 
def is_in_triangle(G, n):
    """
    Checks whether a node `n` in graph `G` is in a triangle relationship or not. 
    
    Returns a boolean.
    """
    in_triangle = False
    
    # Iterate over all possible triangle relationship combinations
    for n1, n2 in combinations(G.neighbors(n), 2): # G.neighbors(n) return a list of the nodes connected to the node n.
    
        # Check if an edge exists between n1 and n2
        if G.has_edge(n1, n2):
            in_triangle = True
            break
    return in_triangle

#function that return all of the graph nodes that are in a triangle_clique
def nodes_in_triangle(G):
    list=[]
    for n in G.nodes():
        if is_in_triangle(G, n):
            list.append(n)
    return list

# return a subgraph with the degree-1 egocentric network of the node n
def degree_1_Network(G, n):        
    vecinos = []
    # Iterate over all possible triangle relationship combinations            
    for m in G.neighbors(n):    
            vecinos.append([n,m])                                       
    return vecinos

#return a subgraph with the degree-1-5 egocentric network of the node
def degree_1_5_Network(G, n):        
    vecinos = []
    # Iterate over all possible triangle relationship combinations            
    for m in G.neighbors(n):    
           for o in G.neighbors(m):
                 if G.has_edge(m,n) :
                    vecinos.append([m,o])
    return vecinos

#return a subgraph with  the degree-2 egocentric network of the node
def degree_2_Network(G, n):        
    vecinos = []
    # Iterate over all possible triangle relationship combinations            
    for m in G.neighbors(n):
            vecinos.append([n,m])
            for o in G.neighbors(m):
                    vecinos.append([m,o])
                    for p in G.neighbors(o):
                        vecinos.append([o,p])
    return vecinos

def main():  
    #se consultan los usuarios de github para el analisis
    try:
        l_usuarios=usuarios()
    except Exception as inst:
        print("##############################")
        print("error al obtener usuarios de la api de github")
        print("##############################")
        return
    #se consultan los seguidores de los usuarios seleccionados
    if seguidores(G, l_usuarios) != "false":
        ##############################
        # se ejecuta después de validar que si existe el grafo de usuarios y seguidores
        # la función seguidores(G,l_usuarios) carga el grafo con el dataset seleccionado.
        # La función seguidores() se ejecuta en la validación que indica si el grafo se creó
        # exitosamente (en este caso la función seguidores() retorna "true", caso contrario
        # retorna "false", es decir, si el grafo se crea correctamente la función retorna "true"
        # y sino retorna "false). Lo anterior antes de permitir hacer cálculos con el grafo
        ##############################
        print("##############################")
        print("si existen usuarios y seguidores. Se ha creado correctamente el dataset y el grafo")
        print("##############################")

        ##############################
        #pintar el grafo con el dataset consultado a github
        plt.figure()
        #nx.draw_networkx(G, [1,2,3], with_labels=False, alpha=0.4,font_size=0.0,node_size=10) 
        nx.draw_networkx(G)
        plt.show()
        plt.savefig("G.png")
        print("##############################")
        print("############ G ###############")
        print(G)  
        print("##############################")
        ##############################

        ##############################
        #pintar los nodos del grafo              
        # plt.figure()        
        # nx.draw_networkx(G.edges())       
        # plt.show() 
        # plt.savefig("G.edges.png")
        print("##############################")
        print("######## G.edges() ###########")
        print(G.edges())  
        print("##############################")
        ##############################

        

        ##############################
        #print(nodeMeasure_density(G))
        ##############################

        ##############################
        try:
            nodeMeasure_degree(G)
        except Exception as inst:
            print("##############################")
            print("error al ejecutar nodeMeasure_degree()")
            print(inst)
            print("##############################")
        ##############################

        ##############################           
        print("##############################")
        print("####### max_cliques() ########")
        print(list(max_cliques(G)))
        try:
            plt.figure()        
            nx.draw_networkx(max_cliques(G))
            plt.show()
            plt.savefig("max_cliques.png")
        except Exception as inst:
            print("##############################")
            print("error al pintar nx.draw_networkx(max_cliques(G)).")
            print(inst)
            print("##############################")

        ##############################
                
        ##############################
        # Extract the subgraph with the nodes of interest: T_draw
        try:
            T_draw = get_nodes_and_nbrs(G, [10, 20])
            plt.figure()
            nx.draw_networkx(T_draw)
            plt.show()
            plt.savefig("get_nodes_and_nbrs.png")
        except Exception as inst:
            print("##############################")
            print("get_nodes_and_nbrs. NetworkXError. The node(nodes) is(are) not in the graph.")
            print("##############################")
                    
        ##############################

        ##############################
        try:
            print("##############################")
            print(is_in_triangle(G,15))
            print("##############################")
            print("##############################")
            print(is_in_triangle(G,3))
            print("##############################")
        except Exception as inst:
            print("##############################")
            print("is_in_triangle. The node is not in the graph")
            print("##############################")
        ##############################        

        #the graph nodes that are in a triangle_clique
        try:
            nodes_in_triangle(T_draw)
        except Exception as inst:
            print("##############################")
            print("nodes_in_triangle. The node is not in the graph")
            print("##############################")
        
        ############################## 
        try:
            print("######## degree_1_Network #########")
            print(degree_1_Network(G, 1))
            print("##############################")
        except Exception as inst:
            print("##############################")
            print("degree_1_Network. There are not subgraph with the degree-1 egocentric network of the node")
            print(inst)
            print("##############################")
        ############################## 

        ############################## 
        try:
            print("######## degree_1_5_Network #########")
            print(degree_1_5_Network(G, 1))
            print("##############################")
        except Exception as inst:
            print("##############################")
            print("degree_1_5_Network. There are not subgraph with the degree-1 egocentric network of the node")
            print(inst)
            print("##############################")
        ##############################

        ############################## 
        try:
            print("######## degree_2_Network #########")
            print(degree_2_Network(G, 1))
            print("##############################")
        except Exception as inst:
            print("##############################")
            print("degree_2_Network. There are not subgraph with the degree-1 egocentric network of the node")
            print(inst)
            print("##############################")
        ##############################
                

    
main()