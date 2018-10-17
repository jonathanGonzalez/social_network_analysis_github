#!flask/bin/python
from flask import Flask
# se importa requests para consumir servicio
import requests
#
import simplejson as json

from networkx.readwrite import json_graph

app = Flask(__name__)
@app.route('/')

def index():
    #response = requests.get("https://api.github.com/search/users?q=+type:user+language:javascript+location:colombia+repos:1")
    #r = requests.get('https://api.github.com/search/users?q=+type:user+language:javascript+location:colombia+repos:1', auth=('jota_q91@hotmail.com', 'github01947'))
    r = requests.get('https://api.github.com/search/users?q=+type:user+language:javascript+location:colombia+repos:1')
    #response = json.loads(r.text)
    data = r.json()
    #response = json.loads(data)
    #print(response.content)    
    # retornar json completo
    return str(data)
    #obtener valor de un campo de la respuesta json
    #return str(data['total_count'])
    #print(str(type(data['items'])))
    #return str(data['items'][0]['login'])       


if __name__ == '__main__':
    app.run(debug=True)