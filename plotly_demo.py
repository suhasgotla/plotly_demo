# Author    : Suhas Gotla
# Purpose   : COMBINE Seminar, PHYS 780, Sep 23, 2020
# Contact   : sgotla@terpmail.umd.edu

# Dependencies:
# - Python 3
# - plotly (install using 'pip install plotly')
# - chart_studio (install using 'pip install chart_studio')

import plotly.graph_objects as go

import networkx as nx

import random

import numpy as np

random.seed(100)

def generateRandomGraphs():
    '''
    Returns a multi-frame plotly graph object
    '''

    # number of nodes in your network
    n             = 50

    # This list will be used to alter positions of the nodes
    decreasing_sd = np.linspace(0.05, 0.3, 20)[::-1]

    edges = []
    nodes = []

    # A dictionary of inital positions for our nodes
    p = {i: (random.gauss(0, 0.7), random.gauss(0, 0.7)) for i in range(n)}


    for sd in decreasing_sd:
        
        
        for i in range(n):
        
            # Change positions of the ndoes based on decreasing_sd

            #p[i] = (p[i][0] + np.random.normal(0, sd), p[i][1] + np.random.normal(0, sd))
            p[i] = (p[i][0] - abs(np.random.normal(0, sd)), p[i][1] - abs(np.random.normal(0, sd)))

        # Create a graph

        G = nx.random_geometric_graph(n, 0.5, pos=p)

        # Join the edges and generate scatter objects

        edge_x = []
        edge_y = []
        for edge in G.edges():
            x0, y0 = G.nodes[edge[0]]['pos']
            x1, y1 = G.nodes[edge[1]]['pos']
            edge_x.append(x0)
            edge_x.append(x1)
            edge_x.append(None)
            edge_y.append(y0)
            edge_y.append(y1)
            edge_y.append(None)

        edge_trace = go.Scatter(
            x=edge_x, y=edge_y,
            line=dict(width=0.5, color='#888'),
            hoverinfo='none',
            mode='lines')

        node_x = []
        node_y = []
        for node in G.nodes():
            x, y = G.nodes[node]['pos']
            node_x.append(x)
            node_y.append(y)

        node_trace = go.Scatter(
            x=node_x, y=node_y,
            mode='markers',
            hoverinfo='text',
            marker=dict(
                showscale=True,
                # colorscale options
                #'Greys' | 'YlGnBu' | 'Greens' | 'YlOrRd' | 'Bluered' | 'RdBu' |
                #'Reds' | 'Blues' | 'Picnic' | 'Rainbow' | 'Portland' | 'Jet' |
                #'Hot' | 'Blackbody' | 'Earth' | 'Electric' | 'Viridis' |
                colorscale='RdBu',
                reversescale=True,
                color=[],
                cmin=0,
                cmax=15,
                size=20,
                colorbar=dict(
                    thickness=15,
                    title='Node Connections',
                    xanchor='left',
                    titleside='right'
                ),
                line_width=2))
    

        ## Colour the nodes based on number on degree

        node_adjacencies = []
        node_text = []
        for node, adjacencies in enumerate(G.adjacency()):
            node_adjacencies.append(len(adjacencies[1]))
            node_text.append('# of connections: '+str(len(adjacencies[1])))

        node_trace.marker.color = node_adjacencies
        node_trace.text = node_text
        
        edges.append(edge_trace) ; nodes.append(node_trace)
        #edge_node_pairs.append( (edge_trace, node_trace) )


    # Create a multi-frame plotly graph object
    fig = go.Figure(
    
    data=[edges[0], nodes[0]],
             
    layout=go.Layout(
    title='<br>Network graph made with Python',
    titlefont_size=16,
    showlegend=False,
    hovermode='closest',
    margin=dict(b=20,l=5,r=5,t=40),

    xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
    yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
    updatemenus=[ dict(type="buttons",
                        buttons=[dict(label="Play",
                                method="animate",
                                args=[None])] ) ]),


    frames = [go.Frame(data = [ edges[i], nodes[i] ]) for i in range(len(decreasing_sd))]
    
    
    )

    return fig

plotly_fig = generateRandomGraphs()

# Uncomment following line to view on local computer
# Plotly will open a browser tab
#plotly_fig.show()


## Following block of code uploads the graph object to your free plotly chart studio account
import chart_studio
import chart_studio.plotly as py 

# Create chart_studio account here: https://plotly.com/api_signup

chart_studio.tools.set_credentials_file(username='yourUserName', api_key='yourAPIkey')

py.plot(plotly_fig, filename="network_demo", auto_open=True)