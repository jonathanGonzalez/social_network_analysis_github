import urllib.request, json 
import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd
from itertools import combinations
from timeit import Timer
import datetime

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
    # print("############## l_usu ###############")
    # print(l_usu)
    # print("#############################")
    #contadorFollowers = 0
    contadorl_usu = 0
    try:
        for u in l_usu:             
            contadorl_usu = contadorl_usu + 1 
            #print("#####contador de ciclos a l_usu()######")                                 
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
                                
                # print("##############################")   
                # print("#####u['login']############")
                # print(u['login'])
                # print("#####s['login']############")
                # print(s['login'])
                # print("##############################") 
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
    print("############## density #############")    
    print(density)
    print("####################################")
    print(density)
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

def centrality(G):
    G = nx.convert_node_labels_to_integers(G,first_label=1)
    degCent = nx.degree_centrality(G)
    #sorted_by_value = sorted(degCent)
    sorted_by_value = sorted(degCent.items(), key=lambda kv: kv[1])
    #sorted_by_value
    # print("############centrality - degCent#################")    
    # print(degCent)
    # print("##############################")
    graphDoc= open("degree_centrality.txt","w+")                   
    graphDoc.write(str(degCent))
    graphDoc.close()   
    # print("###############centrality - sorted_by_value###############")
    # print(sorted_by_value)
    # print("##############################")
    graphDoc= open("degree_centrality_sorted_by_value.txt","w+")                   
    graphDoc.write(str(sorted_by_value))
    graphDoc.close() 

def centralityTopFive(G):
    #G = nx.convert_node_labels_to_integers(G,first_label=1)
    degCent = nx.degree_centrality(G)
    #sorted_by_value = sorted(degCent)
    sorted_by_value = sorted(degCent.items(), key=lambda kv: kv[1], reverse=True)
    top_five=sorted_by_value[0:5]
    graphDoc= open("centralityTopFive.txt","w+")                   
    graphDoc.write(str(top_five))
    graphDoc.close() 
    return top_five

def closenessCentrality(G):
    closeCent = nx.closeness_centrality(G)
    graphDoc= open("closeness_centrality.txt","w+")                   
    graphDoc.write(str(closeCent))
    graphDoc.close() 
    return closeCent

def closenessCentralityTopFive(G):
    closeCent = nx.closeness_centrality(G)
    sorted_by_value = sorted(closeCent.items(), key=lambda kv: kv[1])
    closeness_top_five=sorted_by_value[0:5]    
    graphDoc= open("closeness_centralityTopFive.txt","w+")                   
    graphDoc.write(str(closeness_top_five))
    graphDoc.close()
    return closeness_top_five

def betweennessCentrality(G):
    #G = nx.barbell_graph(m1=5, m2=1)
    betweCent=nx.betweenness_centrality(G)
    graphDoc= open("betweenness_centrality.txt","w+")                   
    graphDoc.write(str(betweCent))
    graphDoc.close()
    #print(betweCent)

def betweennessCentralityTopFive(G):
    betweCent=nx.betweenness_centrality(G)
    sorted_by_value = sorted(betweCent.items(), key=lambda kv: kv[1], reverse=True)
    betweenness_top_five=sorted_by_value[0:5]  
    graphDoc= open("betweenness_top_five_TopFive.txt","w+")                   
    graphDoc.write(str(betweenness_top_five))
    graphDoc.close()  


def eigenvectorCentrality(G):
    eigenCent = nx.eigenvector_centrality(G)
    #print(eigenCent)
    graphDoc= open("eigenvector_centrality.txt","w+")                   
    graphDoc.write(str(eigenCent))
    graphDoc.close()

def eigenvectorCentralityTopFive(G):
    eigenCent = nx.eigenvector_centrality(G)
    #print(eigenCent)    
    sorted_by_value = sorted(eigenCent.items(), key=lambda kv: kv[1], reverse=True)
    eigenvector_top_five=sorted_by_value[0:5]
    graphDoc= open("eigenvector_centrality_topFive.txt","w+")                   
    graphDoc.write(str(eigenvector_top_five))
    graphDoc.close()
    #print(eigenvector_top_five)

def intersection(lst1, lst2):
    lst3 = [value for value in lst1 if value in lst2]
    graphDoc= open("intersection_of_nodes_in_topFive.txt","w+")                   
    graphDoc.write(str(lst3))
    graphDoc.close()    

#maximal-cliques in a graph
def max_cliques(G):    
    #print(list(nx.find_cliques(G)))    
    # print("##############################")
    # print("####### max_cliques() ########")
    # print(list(nx.find_cliques(G)))
    graphDoc= open("find_cliques.txt","w+")                   
    graphDoc.write(str(list(nx.find_cliques(G))))
    graphDoc.close()
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
    graphDoc= open("get_nodes_and_nbrs.txt","w+")                   
    graphDoc.write(str(G.subgraph(nodes_to_draw)))
    graphDoc.close()            
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
    print("############## in_triangle: ################")    
    print(in_triangle)
    print("##############  ################")    
    return in_triangle

#function that return all of the graph nodes that are in a triangle_clique
def nodes_in_triangle(G):
    list=[]
    for n in G.nodes():
        if is_in_triangle(G, n):
            list.append(n)
    # print("############## nodes_in_triangle: ################")    
    # print(list)
    # print("##############  ################") 
    graphDoc= open("nodes_in_triangle.txt","w+")                   
    graphDoc.write(str(list))
    graphDoc.close()      
    return list

# return a subgraph with the degree-1 egocentric network of the node n
def degree_1_Network(G, n):        
    vecinos = []
    # Iterate over all possible triangle relationship combinations            
    for m in G.neighbors(n):    
            vecinos.append([n,m])                                       
    graphDoc= open("degree_1_Network.txt","w+")                   
    graphDoc.write(str(vecinos))
    graphDoc.close() 
    return vecinos

#return a subgraph with the degree-1-5 egocentric network of the node
def degree_1_5_Network(G, n):        
    vecinos = []
    # Iterate over all possible triangle relationship combinations            
    for m in G.neighbors(n):    
           for o in G.neighbors(m):
                 if G.has_edge(m,n) :
                    vecinos.append([m,o])
    graphDoc= open("degree_1_5_Network.txt","w+")                   
    graphDoc.write(str(vecinos))
    graphDoc.close() 
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
    graphDoc= open("degree_2_Network.txt","w+")                   
    graphDoc.write(str(vecinos))
    graphDoc.close() 
    return vecinos

def distanceMeasures(G):
    #print("average",nx.average_shortest_path_length(G)) #Average distance between every pair of nodes.
    print("diameter",nx.diameter(G)) #maximum distance between any pair of nodes.
    print("eccen",nx.eccentricity(G)) #of a node n is the largest distance between n and all other nodes.
    print("radius",nx.radius(G)) #Minimum eccentricity.
    print("periphery",nx.periphery(G)) #Set of nodes that have eccentricity equal to the diameter.
    print("center",nx.center(G)) #set of nodes that have eccentricity equal to the radius.

def draw(graph_to_draw, nameOfDraw):
    try:
        plt.figure()
        nx.draw_networkx(graph_to_draw)
        plt.show()
        plt.savefig(nameOfDraw + datetime.datetime.now() +"x.png")        
    except Exception as inst:
        print("##############################")
        print("error al crear gráfica:")
        print(nameOfDraw)
        print(inst)
        print("##############################")

def graph_is_connected(G):
    print("############## is_connected: ################")    
    print(nx.is_connected(G))
    print("##############  ################")    

def graph_number_connected_components(G):
    #G.remove_node(0) 
    print("############## number_connected_components ################")    
    print(nx.number_connected_components(G))
    print("#############################")
    #print("############## sorted connected_components ################")    
    #print(sorted(nx.connected_components(G)))
    #print("#############################")
    graphDoc= open("sorted_connected_components.txt","w+")                   
    graphDoc.write(str(sorted(nx.connected_components(G))))
    graphDoc.close()    

print(sorted(nx.connected_components(G))) 

def simplePaths(G):
    G.nodes()
    paths=nx.all_simple_paths(G, source=9, target=26)
    type(paths)
    print("############## all_simple_paths ################")    
    print(paths)
    print("#############################")

def draw2(G, nameOfDraw):    
    try:
        pos = nx.get_node_attributes(G, 'login')    
        plt.figure()        
        nx.draw_networkx(G, pos)
        plt.show()
        plt.savefig(nameOfDraw + datetime.datetime.now() +"x.png")        
    except Exception as inst:
        print("##############################")
        print("error al crear gráfica:")
        print(nameOfDraw)
        print(inst)
        print("##############################")

def draw3(G, nameOfDraw):    
    try:                        
        plt.figure(figsize=(10,7))
        nx.draw_networkx(G, alpha=0.7, with_labels=False, edge_color='.4')
        plt.axis('off')
        plt.tight_layout()
        plt.show()
        plt.savefig(nameOfDraw + datetime.datetime.now() +"x.png")        
    except Exception as inst:
        print("##############################")
        print("error al crear gráfica:")
        print(nameOfDraw)
        print(inst)
        print("##############################")

def draw4(G, nameOfDraw):
    try:                        
        plt.figure()
        nx.draw_networkx(G)        
        plt.tight_layout()
        plt.show()
        plt.savefig(nameOfDraw + datetime.datetime.now() +"x.png")        
    except Exception as inst:
        print("##############################")
        print("error al crear gráfica:")
        print(nameOfDraw)
        print(inst)
        print("##############################")

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

        try:
            graph_is_connected(G)
        except Exception as inst:
            print("##############################")
            print("error al ejecutar graph_is_connected()")
            print(inst)
            print("##############################")
        ##############################     
                
        try:
            graph_number_connected_components(G)
        except Exception as inst:
            print("##############################")
            print("error al ejecutar graph_is_connected()")
            print(inst)
            print("##############################")   

        try:
            simplePaths(G)
        except Exception as inst:
            print("##############################")
            print("error al ejecutar simplePaths()")
            print(inst)
            print("##############################")

        ##############################
        #pintar el grafo con el dataset consultado a github
        # plt.figure()
        # #nx.draw_networkx(G, [1,2,3], with_labels=False, alpha=0.4,font_size=0.0,node_size=10) 
        # nx.draw_networkx(G)    
        # plt.savefig("G.png")
        # plt.show()
        draw(G, "grafo")
        draw3(G, "grafo-tight_layout")

        print("##############################")
        print("############ G ###############")
        print(G)
        graphDoc= open("network-graph.txt","w+")                   
        graphDoc.write(str(G))
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
        graphDoc= open("network-graph_edges.txt","w+")                   
        graphDoc.write(str(G.edges()))
        graphDoc.close()
        draw(G.edges(), "G.edges()")
        print("##############################")
        ##############################

        

        ##############################        
        try:
            nodeMeasure_density(G)
        except Exception as inst:
            print("##############################")
            print("error al ejecutar nodeMeasure_density()")
            print(inst)
            print("##############################")
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
        
        try:
            centrality(G)
        except Exception as inst:
            print("##############################")
            print("error al ejecutar centrality():")
            print(inst)
            print("##############################")
        ##############################

        try:
            centralityTopFive(G)
        except Exception as inst:
            print("##############################")
            print("error al ejecutar centralityTopFive():")
            print(inst)
            print("##############################")
        ##############################
        try:
            betweennessCentrality(G)
        except Exception as inst:
            print("##############################")
            print("error al ejecutar betweennessCentrality():")
            print(inst)
            print("##############################")
        ##############################            
        ##############################
        try:
            betweennessCentralityTopFive(G)
        except Exception as inst:
            print("##############################")
            print("error al ejecutar betweennessCentralityTopFive():")
            print(inst)
            print("##############################")
        ############################## 

        ##############################
        try:
            eigenvectorCentrality(G)
        except Exception as inst:
            print("##############################")
            print("error al ejecutar eigenvectorCentrality():")
            print(inst)
            print("##############################")
        ##############################              
        
        try:
            eigenvectorCentralityTopFive(G)
        except Exception as inst:
            print("##############################")
            print("error al ejecutar eigenvectorCentralityTopFive():")
            print(inst)
            print("##############################")
        ##############################          

        try:
            closenessCentrality(G)
        except Exception as inst:
            print("##############################")
            print("error al ejecutar closenessCentrality():")
            print(inst)
            print("##############################")
        ##############################
        
        try:
            closenessCentralityTopFive(G)
        except Exception as inst:
            print("##############################")
            print("error al ejecutar closenessCentralityTopFive():")
            print(inst)
            print("##############################")
        ##############################
                 
        try:
            intersection(closenessCentralityTopFive(G), centralityTopFive(G))            
        except Exception as inst:
            print("##############################")
            print("error al ejecutar intersection():")
            print(inst)
            print("##############################")
        
        ##############################                   
        try:
            # plt.figure()        
            # nx.draw_networkx(max_cliques(G))
            # plt.show()
            # plt.savefig("max_cliques.png")
            draw(max_cliques(G), "max_cliques")
        except Exception as inst:
            print("##############################")
            print("Exception nx.draw_networkx(max_cliques(G)).")
            print(inst)
            print("##############################")

        ##############################
                
        ##############################
        # Extract the subgraph with the nodes of interest: T_draw
        try:
            T_draw = get_nodes_and_nbrs(G, ['angelbotto'])
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
            print("###############is_in_triangle###############")
            print(is_in_triangle(G, "angelbotto"))            
            # print("##############################")
            # print(is_in_triangle(G,6))
            print("##############################")
        except Exception as inst:
            print("##############################")
            print("exception in is_in_triangle.")
            print(inst)
            print("##############################")
        ##############################        

        #the graph nodes that are in a triangle_clique
        try:
            nodes_in_triangle(G)
        except Exception as inst:
            print("##############################")
            print("exception in nodes_in_triangle")
            print(inst)
            print("##############################")
        
        ############################## 
        try:
            print("######## degree_1_Network #########")
            print(degree_1_Network(G, "angelbotto"))
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
            print(degree_1_5_Network(G, "angelbotto"))
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
            print(degree_2_Network(G, 'angelbotto'))
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

        ############################## 
        try:            
            draw2(max_cliques(G), "max_cliques")            
        except Exception as inst:
            print("##############################")
            print("draw2 max_cliques Exception")
            print(inst)
            print("##############################")
        ##############################

        ############################## 
        try:            
            draw3(G, "draw3")            
        except Exception as inst:
            print("##############################")
            print("draw3 Exception")
            print(inst)
            print("##############################")
        ##############################

        ############################## 
        try:            
            draw4(G, "draw4")            
        except Exception as inst:
            print("##############################")
            print("draw4 Exception")
            print(inst)
            print("##############################")
        ##############################
                    
main()