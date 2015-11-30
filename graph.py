import networkx as nx

subs = {
    'santa': 'sta',
    'plaza': 'pza',
    'universidad': 'univ',
    'distribuidor': 'dist'
}

graph_description = [
    {
        'from': 'El Cafetal',
        'to': 'Los Ruices',
        'keywords': ['San Luis','Santa Paula','Santa Marta','Santa Sofia',
                     'Cafetal','Bulevard','Raul Leoni', 'Boulevard',
                     'Bulevar', 'Boulevar'],
        'tiempo': 10,
        'p': lambda x: 12.5 * (x**2)
    },
    {
        'from': 'El Cafetal',
        'to': 'Vizcaya',
        'keywords':  ['Vizcaya','La Guairita'],
        'tiempo': 3,
        'p': lambda x: 10*x
    },
    {
        'from': 'El Cafetal',
        'to': 'Los Naranjos',
        'keywords':  ['Plaza las Americas','Los Naranjos'],
        'tiempo': 10,
        'p': lambda x: 15*x
    },
    {
        'from': 'Los Naranjos',
        'to': 'El Hatillo',
        'keywords':  ['Hatillo','Universidad Nueva Esparta', 'UNE', 'La Muralla',
                      'Tocuyito'],
        'tiempo': 15,
        'p': lambda x: 10*x
    },
    {
        'from': 'El Hatillo',
        'to': 'El Volcan',
        'keywords':  ['Kavak','Volcan'],
        'tiempo': 15,
        'p': lambda x: 10*x
    },
    {
        'from': 'El Volcan',
        'to': 'El Placer',
        'keywords':  ['Oripoto','Gavilan','Jean Piglet'],
        'tiempo': 10,
        'p': lambda x: 7.5*x
    },
    {
        'from': 'El Placer',
        'to': 'USB',
        'keywords':  ['El Placer', 'USB', 'Universidad Simon Bolivar'],
        'tiempo': 5,
        'p': lambda x: 8*x
    },
    {
        'from': 'Hoyo de la Puerta',
        'to': 'USB',
        'keywords':  ['Hoyo de la Puerta', 'HDLP',
                      'USB', 'Universidad Simon Bolivar'],
        'tiempo': 10,
        'p': lambda x: 10 * x * x + 5*x
    },
    {
        'from': 'La Rinconada',
        'to': 'Hoyo de la Puerta',
        'keywords':  ['Tazon','La Rinconada','Charallave','La Victoria', 'Basurero',
                      'Valencia','Valles del Tuy','Ocumitos','Las Mayas','ARC'],
        'tiempo': 15,
        'p': lambda x: 15*x*x,
    },
    {
        'from': 'Distribuidor AFF',
        'to': 'La Rinconada',
        'keywords':  ['Valle-Coche', 'Valle', 'Coche',
                      'VC','El Pulpo','Santa Monica','Proceres',
                      'Chaguaramos','La Bandera'],
        'tiempo': 20,
        'p': lambda x: 20*x
    },
    {
        'from': 'Los Ruices',
        'to': 'Distribuidor AFF',
        'keywords':  ['Francisco Fajardo', 'AFF','El Pulpo','La Polar',
                      'Santa Cecilia',
                      'Distribuidor Altamira','Soto'],
        'tiempo': 10,
        'p': lambda x: 25*x
    },
    {
        'from': 'Vizcaya',
        'to': 'Los Samanes',
        'keywords':  ['Los Samanes','La Guairita'],
        'tiempo': 10,
        'p': lambda x: 10*x
    },
    {
        'from': 'Los Samanes',
        'to': 'La Trinidad',
        'keywords':  ['Los Samanes','La Trinidad','Procter', 'Gamble'],
        'tiempo': 10,
        'p': lambda x: 10*x
    },
    {
        'from': 'Distribuidor AFF',
        'to': 'La Trinidad',
        'keywords':  ['Prados del Este', 'Prados', 'PDE','Santa Fe','Concresa',
                      'Santa Rosa de Lima', 'Santa Rosa','Ciempies','Valle Arriba',
                      'Terrazas','Los Campitos', 'Tunel de la Trinidad'],
        'tiempo': 15,
        'p': lambda x: 20*x
    },
    {
        'from': 'La Trinidad',
        'to': 'Piedra Azul',
        'keywords':  ['Baruta','EPA','La Trinidad','Expreso'],
        'tiempo': 10,
        'p': lambda x: 8*x
    },
    {
        'from': 'Piedra Azul',
        'to': 'El Placer',
        'keywords':  ['El Placer','Los Guayabitos','Ojo de Agua','Monterrey'],
        'tiempo': 10,
        'p': lambda x: 13*x
    },
    {
        'from': 'La Trinidad',
        'to': 'El Hatillo',
        'keywords':  ['La Trinidad','El Hatillo','La Boyera'],
        'tiempo': 15,
        'p': lambda x: 13*x
    },
]

def transform(keywords):
    new_keywords = []
    for keyword in keywords:
        new_keywords.append(keyword)
        for (k, v) in subs.items():
            new_keyword = keyword.replace(k, v)
            if new_keyword != keyword:
                new_keywords.append(new_keyword)
    return new_keywords

def get_graph():
    g = nx.Graph()
    for edge in graph_description:
        keywords = transform([x.strip().lower() for x in edge['keywords']])
        g.add_edge(edge['from'], edge['to'],
                   {
                       'keywords': keywords,
                       'tiempo': edge['tiempo'],
                       'p': edge['p']
                   })

    return g

graph = get_graph()
print graph.edges()

for (x,y) in graph.edges():
	print graph.edge[x][y]['tiempo']
