import pandas as pd
import networkx as nx
import random
from pathlib import Path
import src.graph.Metrics as Met


def random_walk(graph):
    # node_couts = {}
    return graph


def random_node_id(nodes):
    return random.choice(nodes)


def next_step(node, graph):
    print(graph.edges(node))
    print(len(graph.edges(node)))
    print(1/len(graph.edges(node)))
    return graph.edges(node)


def initialize_graph():
    my_file = Path("../../data/graph.p")

    if my_file.is_file():
        graph = nx.read_gpickle(my_file)
    else:
        df = pd.read_csv('../../data/processed/products_nodes_links.csv', sep=';')
        df.columns = ['node1', 'node2']

        graph = nx.Graph()
        for i in range(0, len(df.index)):
            graph.add_edge(str(df.node1[i]), str(df.node2[i]))

        nx.write_gpickle(graph, my_file)

    return graph

def initialize_largest_connected_subgraph():
    # check if file already exists, then load, otherwise generate
    largest_cc_file = Path("../../data/processed/largest_cc_subgraph.p")

    if largest_cc_file.is_file():
        largest_cc_subgraph = nx.read_gpickle(largest_cc_file)
    else:
        full_graph = initialize_graph()
        # find the largest connected component and use it to construct subgraph
        largest_cc = max(nx.connected_components(full_graph), key=len)
        largest_cc_subgraph = full_graph.subgraph(largest_cc)
        # Save graph
        nx.write_gpickle(largest_cc_subgraph, largest_cc_file)
    return largest_cc_subgraph


if __name__ == '__main__':

    g = initialize_largest_connected_subgraph()

    n = list(g.nodes)

    print(random_node_id(n))

    # Met.print_connected_components(g)

    Met.print_metrics(g)
