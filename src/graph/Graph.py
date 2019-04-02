import pandas as pd
import networkx as nx
import random
from pathlib import Path
import graph.Metrics as Met
import operator


def random_walk(graph, it, steps):

    # initialize the node count dictionary with 0 counts
    node_counts = {node_ids: 0 for node_ids in list(graph.nodes)}

    for i in range(0, it):

        prev_node = random_node_id(list(graph.nodes))

        for step in range(0, steps):

            node_counts[str(prev_node)] += 1

            ns = next_step(prev_node, graph)

            prev_node = ns

    return node_counts


def random_node_id(nodes):
    return random.choice(nodes)


def next_step(node, graph):
    return random_node_id([n[1] for n in list(graph.edges(node))])


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


def write_to_csv(path, output):
    pd.DataFrame.from_dict(output, orient='index', columns=['number_of_visits']) \
        .sort_values(by='number_of_visits', ascending=False)\
        .to_csv(path)


if __name__ == '__main__':

    _g = initialize_graph()

    res = random_walk(_g, 100, 10000)

    write_to_csv("../../data/results/full_random_walk.csv", res)

    # Met.print_metrics(_g)
