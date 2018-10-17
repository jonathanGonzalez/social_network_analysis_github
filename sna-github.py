import urllib.request, json 
import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd

import warnings
warnings.filterwarnings('ignore')

G = nx.Graph()

def usuarios():	
    url1='https://api.github.com/search/users?q=+type:user'
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
                print("error de conexión")
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
    G = nx.convert_node_labels_to_integers(G,first_label=1)
    degree_sequence=sorted(nx.degree(G).values(),reverse=True)     
    dmax=max(degree_sequence) 
    dmin =min(degree_sequence)

    print(degree_sequence)
    print(dmax)
    print(dmin)

#maximal-cliques in a graph
def max_cliques(G):
    nx.find_cliques(G)    
    plt.figure()
    #nx.draw_networkx(G, pos, with_labels=False, alpha=0.4,font_size=0.0,node_size=10) 
    nx.draw_networkx(G)
    plt.savefig("max_cliques.png")
    print(list(nx.find_cliques(G)))

def main():
    #print(usuarios())
    #if(usuarios())
    l_usuarios=usuarios()
    #print(type(l_usuarios))
    #print("l_usuarios = ")
    #print(l_usuarios)
    #print(l_usuarios[0]['login'])
    #print(seguidores(G, l_usuarios))   
    if seguidores(G, l_usuarios) != "false":
        print("si hay seguidores")
        #seguidores(G,l_usuarios)
        print(nodeMeasure_density(G))
        #nodeMeasure_degree(G)
        max_cliques(G)
    #print(G.edges())
    #nx.draw_networkx(G.edges())

main()