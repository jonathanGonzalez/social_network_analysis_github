import urllib.request, json 
import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd
from itertools import combinations
from timeit import Timer

import warnings
warnings.filterwarnings('ignore')


G = nx.Graph()


def usuarios():	
    #url1='https://api.github.com/search/users?q=+type:user+location:colombia'
    url1='https://api.github.com/search/users?q=+type:user+location:colombia+repos:>10+language:javascript&per_page=50'
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
    userDoc= open("users.txt","w+")
    userDoc.write(str(users['items']))
    userDoc.close() 
    return users['items']

def seguidores(G, l_usu):
    print("############## l_usu ###############")
    print(l_usu)
    print("#############################")
    contadorFollowers = 0
    contadorl_usu = 0
    try:
        for u in l_usu:             
            contadorl_usu = contadorl_usu + 1 
            print("#####contador de ciclos a l_usu()######")                                 
            #Timer.timeit(10.0, print(contadorl_usu))            
            print(contadorl_usu)
            print("##############################")                   
            url_seg2=u['followers_url']             
            try:       
                with urllib.request.urlopen(url_seg2) as url:
                    seguid= json.loads(url.read().decode()) 
                    
            except Exception as inst:   
                print("#####función seguidores()######")             
                print("error de conexión")
                print(inst)
                print("##############################")
                return "false"  
            FollowersDoc= open("seguidores.txt","w+")                   
            FollowersDoc.write(str(seguid))
            FollowersDoc.close()              
            # for item in seguid:
            #     #del item['login']
            #     del item['id']
            #     del item['node_id']	
            #     del item['avatar_url']
            #     del item['gravatar_id']
            #     del item['url']
            #     del item['html_url']
            #     del item['followers_url']
            #     del item['following_url']
            #     del item['gists_url']
            #     del item['starred_url']
            #     del item['subscriptions_url']
            #     del item['organizations_url']
            #     del item['repos_url']
            #     del item['events_url']
            #     del item['received_events_url']
            #     del item['type']
            #     del item['site_admin']		
            for s in seguid:
                # contadorFollowers = contadorFollowers + 1
                # print("#####contador de llamdos a follower()######")                                 
                # print(contadorFollowers)
                # print("##############################")
                
                G.add_edge(u['login'],s['login'])
                                
                print("##############################")   
                print("#####u['login']############")
                print(u['login'])
                print("#####s['login']############")
                print(s['login'])
                print("##############################") 
                # for f in s['items']:                
                #     url_seg2=f['followers_url']             
                #     try:       
                #         with urllib.request.urlopen(url_seg2) as url:
                #             githubUsers= json.loads(url.read().decode())                            
                #     except Exception as inst: 
                #         print("##############################")
                #         print("error al consultar followerFromInitUser")
                #         print(inst)
                #         print("##############################")
                #     for followerFromInitUser in githubUsers:
                #         G.add_edge(s['login'],followerFromInitUser['login'])                        
                #         print("########followerFromInitUser#######")   
                #         print("#####u['login']############")
                #         print(s['login'])
                #         print("#####s['login']############")
                #         print(followerFromInitUser['login'])
                #         print("##############################")               
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

def distanceMeasures(G):
    #print("average",nx.average_shortest_path_length(G)) #Average distance between every pair of nodes.
    print("diameter",nx.diameter(G)) #maximum distance between any pair of nodes.
    print("eccen",nx.eccentricity(G)) #of a node n is the largest distance between n and all other nodes.
    print("radius",nx.radius(G)) #Minimum eccentricity.
    print("periphery",nx.periphery(G)) #Set of nodes that have eccentricity equal to the diameter.
    print("center",nx.center(G)) #set of nodes that have eccentricity equal to the radius.

def main():  
    #se consultan los usuarios de github para el analisis
    try:
        l_usuarios=usuarios()
    except Exception as inst:
        print("##############################")
        print("error al obtener usuarios de la api de github")
        print(inst)
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
        plt.savefig("G.png")
        plt.show()
        print("##############################")
        print("############ G ###############")
        print(G)
        graphDoc= open("graph.txt","w+")                   
        graphDoc.write(print(G))
        graphDoc.close()      
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
        graphDoc= open("graph_edges.txt","w+")                   
        graphDoc.write(str(G.edges()))
        graphDoc.close()
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
            print("exception in get_nodes_and_nbrs")
            print(inst)
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
            print("exception in is_in_triangle.")
            print(inst)
            print("##############################")
        ##############################        

        #the graph nodes that are in a triangle_clique
        try:
            nodes_in_triangle(T_draw)
        except Exception as inst:
            print("##############################")
            print("exception in nodes_in_triangle")
            print(inst)
            print("##############################")
        
        ############################## 
        try:
            print("######## degree_1_Network #########")
            print(degree_1_Network(G, 1))
            print("##############################")
        except Exception as inst:
            print("##############################")
            print("exception degree_1_Network")
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

        ############################## 
        try:
            print("######## DistanceMeasures #########")
            distanceMeasures(G)
            print("##############################")
        except Exception as inst:
            print("##############################")
            print("DistanceMeasures Exception")
            print(inst)
            print("##############################")
        ##############################
                    
main()