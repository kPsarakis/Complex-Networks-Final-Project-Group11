import pandas as pd
import networkx as nx
import src.graph.Metrics as Met

df = pd.read_csv('../../data/processed/products_nodes_links.csv', sep=';')
df.columns = ['node1', 'node2']

G = nx.Graph()

for i in range(0, len(df.index)):
    G.add_node(str(df.node1[i]))
    G.add_node(str(df.node2[i]))
    G.add_edge(str(df.node1[i]), str(df.node2[i]))

# Met.print_metrics(G)


def random_walk(g):
    return g
