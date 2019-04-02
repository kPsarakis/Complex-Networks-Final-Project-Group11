import pandas as pd
import networkx as nx
import random
import src.graph.Metrics as Met

df = pd.read_csv('../../data/processed/products_nodes_links.csv', sep=';')
df.columns = ['node1', 'node2']

G = nx.Graph()

for i in range(0, len(df.index)):
    G.add_edge(str(df.node1[i]), str(df.node2[i]))

nodes = G.nodes

Met.print_metrics(G)


def random_walk(g):
    node_couts = {}
    return g


def random_node_id(n):
    return random.choice(n)


def adjnodes():
    return 0
