import pandas as pd
import networkx as nx
import random
from pathlib import Path
from tqdm import tqdm, trange
import numpy as np


def random_walk(graph, it, steps, param):

    # initialize the node count dictionary with 0 counts
    node_counts = {node_ids: 0 for node_ids in list(graph.nodes)}

    prev_node = None

    if param == "rw":
        dis = False
    else:
        dis = True

    for i in tqdm(range(0, it), total=it, disable=(not dis)):

        if param == "rw":
            prev_node = random_node_id(list(graph.nodes))
        elif param == "grw":
            prev_node = generalized_random_node_id([n[1] for n in list(graph.edges(random_node_id(list(graph.nodes))))],
                                                   node_counts)

        for step in tqdm(range(0, steps), total=steps, disable=dis):

            node_counts[str(prev_node)] += 1

            ns = next_step(prev_node, graph, node_counts, param)

            prev_node = ns

    node_counts = {k: (v/(it*steps)) for k, v in node_counts.items()}

    return node_counts


def random_walk_with_node_removal(graph, it, steps, param, node_counts):

    df = sort_dict(node_counts)

    n = int(len(node_counts.keys())*0.01)

    # top_graph contains the new graph with the top 1% nodes removed
    top = df.head(n=n).index.values
    top_graph = graph.copy()
    remove_nodes(top_graph, top)

    # bot_graph contains the new graph with the top 1% nodes removed
    bot_graph = graph.copy()
    bot = df.tail(n=n).index.values
    remove_nodes(bot_graph, bot)

    # base_graph contains the new graph with the top 1% nodes removed
    base_graph = graph.copy()
    base = df.sample(n=n).index.values
    remove_nodes(base_graph, base)

    rw_top = random_walk(top_graph, it, steps, param)
    write_to_csv("../../data/results/"+param+"_3top.csv", rw_top)

    rw_bot = random_walk(bot_graph, it, steps, param)
    write_to_csv("../../data/results/"+param+"_3bot.csv", rw_bot)

    rw_base = random_walk(base_graph, it, steps, param)
    write_to_csv("../../data/results/"+param+"_3base.csv", rw_base)

    n2_top = calc_norm1(node_counts, rw_top)
    print("Norm1 distance of the new graph to the original graph with the top 1% influential nodes removed: ", n2_top)
    n2_base = calc_norm1(node_counts, rw_base)
    print("Norm1 distance of the new graph to the original graph with random 1% nodes removed: ", n2_base)
    n2_bot = calc_norm1(node_counts, rw_bot)
    print("Norm1 distance of the new graph to the original graph with the bottom 1% influential nodes removed: "
          , n2_bot)


def generalized_random_node_id(nodes, counts: dict):
    # vi(t)
    val = {str(k): counts[str(k)] for k in nodes}
    # sum aij*vj(t)
    s = sum(val.values())
    # dj
    d = len(nodes)
    # pi(t)
    p = {k: (v+1)/(s+d) for k, v in val.items()}

    return random.choices(population=list(p.keys()), weights=list(p.values()))[0]


def random_node_id(nodes):
    return random.choice(nodes)


def next_step(node, graph, node_counts, param):
    if param == "rw":
        return random_node_id([n[1] for n in list(graph.edges(node))])
    elif param == "grw":
        return generalized_random_node_id([n[1] for n in list(graph.edges(node))], node_counts)


def initialize_graph():
    my_file = Path("../../data/processed/sample_10000n_1.p")

    if my_file.is_file():
        graph = nx.read_gpickle(my_file)
    else:
        print("ERROR you should read the pickle file!!!!")
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


def sort_dict(d):
    return pd.DataFrame.from_dict(d, orient='index', columns=['number_of_visits'])\
        .sort_values(by='number_of_visits', ascending=False)


def remove_nodes(graph, nodes):
    for n in list(nodes):
        graph.remove_node(n)


def calc_norm1(orig, rem):

    o = pd.DataFrame.from_dict(orig, orient='index', columns=['visit_frequency'])
    n = pd.DataFrame.from_dict(rem, orient='index', columns=['visit_frequency'])

    j = o.merge(n, how='outer', left_index=True, right_index=True)
    j.columns = ['original', 'new']
    j = j[pd.notnull(j['new'])]

    return sum(abs(j['original'] - j['new']))


if __name__ == '__main__':

    _g = initialize_graph()  # initialize the graph

    init_rand_points = 1
    iterations = int(1e7)  # 10 million
    print("Starting random walk")
    res = random_walk(_g, init_rand_points, iterations, "rw")  # initialize the graph generic random walk
    write_to_csv("../../data/results/final_random_walk.csv", res)
    random_walk_with_node_removal(_g, init_rand_points, iterations, "rw", res)

    _g = initialize_graph()  # initialize the graph

    init_rand_points = 1000
    iterations = int(1e4)  # 10 thousand
    print("Starting generalized random walk")
    res = random_walk(_g, init_rand_points, iterations, "grw")  # initialize the graph generic random walk
    write_to_csv("../../data/results/final_generalized_random_walk.csv", res)
    random_walk_with_node_removal(_g, init_rand_points, iterations, "grw", res)
