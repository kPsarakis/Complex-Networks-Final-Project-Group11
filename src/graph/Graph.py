import pandas as pd
import networkx as nx
import random
from pathlib import Path
from tqdm import tqdm


def random_walk(graph: nx.Graph, it, steps, mode):
    """""
    Function that contains the main functionality for the random walk and generalized random walk algorithms 
    
    :arg graph: The networkX graph object containing the graph
    :arg it: Number of initial random points 
    :arg steps: Number of steps in each initial random point iteration 
    :arg mode: either 'rw' for random walk or 'grw' for generalized random walk 
    
    :returns: The node popularity distribution 
    """""
    # Check if the parameter
    if mode != "rw" and mode != "grw":
        print("The parameter must be either 'rw' for random walk or 'grw' for generalized random walk")
        return None

    # Initialize the node count dictionary with 0 counts
    node_counts = {node_ids: 0 for node_ids in list(graph.nodes)}

    # Initialize the variable holding the previous node
    prev_node = None

    # Loop with progress bar for the number of initial random points
    for _ in tqdm(range(0, it), total=it, disable=(mode == "rw")):

        # If we are at the random walk setting
        if mode == "rw":
            # Pick a random node
            prev_node = random_node_id(list(graph.nodes))
        # If we are at the generalized random walk setting
        elif mode == "grw":

            # Loop that makes sure we do not pick a disconnected node after the removal
            while True:

                # The edges of the chosen node
                edg = [n[1] for n in list(graph.edges(random_node_id(list(graph.nodes))))]

                # If its connected
                if len(edg) != 0:
                    # Get the node and do the Node probability calculation for the generalized random walk
                    prev_node = generalized_random_node_id(edg, node_counts)
                    break

        # Loop with progress bar for the number of steps in each initial random point iteration
        for _ in tqdm(range(0, steps), total=steps, disable=(mode != "rw")):

            # Increase the counter
            node_counts[str(prev_node)] += 1

            # Get the next node of the walk
            ns = next_step(prev_node, graph, node_counts, mode)

            # After the computations set the current node as the previous node
            prev_node = ns

    # Normalize the counts based on the number of random initial points and iterations
    # so, we have the node popularity distribution
    node_counts = {k: (v/(it*steps)) for k, v in node_counts.items()}

    # Return the node popularity distribution
    return node_counts


def random_walk_with_node_removal(graph: nx.Graph, it, steps, mode, node_counts):
    """""
    Function that contains the main functionality for the random walk and generalized random walk algorithms 
    with node removal

    :arg graph: The networkX graph object containing the graph
    :arg it: Number of initial random points 
    :arg steps: Number of steps in each initial random point iteration 
    :arg mode: either 'rw' for random walk or 'grw' for generalized random walk 

    :returns: Nothing (just calls the above random walk function) 
    """""
    # Sort the node visiting frequencies
    df = sort_dict(node_counts)

    # Get the number of the 1% of the nodes
    n = int(len(node_counts.keys())*0.01)

    # top_graph contains the new graph with the top 1% nodes removed
    top = df.head(n=n).index.values
    top_graph = graph.copy()
    remove_nodes(top_graph, top)
    rw_top = random_walk(top_graph, it, steps, mode)
    write_to_csv("../../data/results/" + mode + "_3top.csv", rw_top)

    # bot_graph contains the new graph with the top 1% nodes removed
    bot_graph = graph.copy()
    bot = df.tail(n=n).index.values
    remove_nodes(bot_graph, bot)

    rw_bot = random_walk(bot_graph, it, steps, mode)
    write_to_csv("../../data/results/" + mode + "_3bot.csv", rw_bot)

    # base_graph contains the new graph with the top 1% nodes removed
    base_graph = graph.copy()
    base = df.sample(n=n).index.values
    remove_nodes(base_graph, base)

    rw_base = random_walk(base_graph, it, steps, mode)
    write_to_csv("../../data/results/"+mode+"_3base.csv", rw_base)

    # Calculate and print the norm 1 distances of the graphs after removal compared t the original
    n1_top = calc_norm1(node_counts, rw_top)
    print("Norm1 distance of the new graph to the original graph with the top 1% influential nodes removed: ", n1_top)
    n1_base = calc_norm1(node_counts, rw_base)
    print("Norm1 distance of the new graph to the original graph with random 1% nodes removed: ", n1_base)
    n1_bot = calc_norm1(node_counts, rw_bot)
    print("Norm1 distance of the new graph to the original graph with the bottom 1% influential nodes removed: "
          , n1_bot)


def generalized_random_node_id(nodes, counts: dict):
    """""
    Function that returns a random node for the next step of the generalized random walk

    :arg nodes: The adjacent nodes
    :arg counts: The amount of visits in every node up until the current iteration

    :returns: A random node based on the generalized random walk visiting distribution
    """""
    # vi(t)
    val = {str(k): counts[str(k)] for k in nodes}
    # sum aij*vj(t)
    s = sum(val.values())
    # dj
    d = len(nodes)
    # pi(t)
    p = {k: (v+1)/(s+d) for k, v in val.items()}

    # Return the random node based on the generalized random walk visiting distribution
    return random.choices(population=list(p.keys()), weights=list(p.values()))[0]


def random_node_id(nodes):
    """""
    Function that returns a random node for the next step of the random walk 

    :arg nodes: The adjacent nodes

    :returns: A random node from the adjacent nodes
     """""
    return random.choice(nodes)


def next_step(node, graph, node_counts, mode):
    """""
    Function that returns a random node for the next step of the random walk 

    :arg node: The current node
    :arg graph: The networkX graph object containing the graph
    :arg node_counts: The amount of visits in every node up until the current iteration
    :arg mode: either 'rw' for random walk or 'grw' for generalized random walk 
    
    :returns: A random node from the adjacent nodes
    """""
    if mode == "rw":
        return random_node_id([n[1] for n in list(graph.edges(node))])
    elif mode == "grw":
        return generalized_random_node_id([n[1] for n in list(graph.edges(node))], node_counts)


def initialize_graph():
    """""
    Function that creates a graph either from a pre-constructed pickle file of from a csv that contains the nodes  

    :returns: A random node from the adjacent nodes
    """""
    # The pickle file containing the final proceeded  Graph
    my_file = Path("../../data/processed/sample_10000n_1.p")

    # If the pickle file exists
    if my_file.is_file():
        graph = nx.read_gpickle(my_file)  # Create the graph from the pickle file
    else:
        # Initialize the graph from the csv file
        df = pd.read_csv('../../data/processed/products_nodes_links.csv', sep=';')
        df.columns = ['node1', 'node2']

        graph = nx.Graph()
        for i in range(0, len(df.index)):
            graph.add_edge(str(df.node1[i]), str(df.node2[i]))

        # Create the pickle file to improve runtime in next iterations
        nx.write_gpickle(graph, my_file)

    return graph


def write_to_csv(path, output):
    """""
    Function that writes a dictionary containing the node popularity distributions 

    :arg path: The of the output file
    :arg output: The dictionary containing the node popularity distributions
    """""
    pd.DataFrame.from_dict(output, orient='index', columns=['number_of_visits']) \
        .sort_values(by='number_of_visits', ascending=False)\
        .to_csv(path)


def sort_dict(d):
    """""
    Helper function that sorts a dictionary 

    :arg d: The dictionary
    :returns: The sorted dictionary 
    """""
    return pd.DataFrame.from_dict(d, orient='index', columns=['number_of_visits'])\
        .sort_values(by='number_of_visits', ascending=False)


def remove_nodes(graph, nodes):
    """""
    Function that removes nodes from a graph 

    :arg graph: The networkX object containing the graph
    :arg nodes: The nodes that we want to remove from the graph
    """""
    for n in list(nodes):
        graph.remove_node(n)


def calc_norm1(orig, rem):
    """""
    Function that removes nodes from a graph 

    :arg orig: The original graph distribution
    :arg rem: The graph distribution after the removal
    """""
    o = pd.DataFrame.from_dict(orig, orient='index', columns=['visit_frequency'])
    n = pd.DataFrame.from_dict(rem, orient='index', columns=['visit_frequency'])

    # Join the pandas tables on node id so the table becomes |Node Id| Original Frequency | Frequency after removal
    j = o.merge(n, how='outer', left_index=True, right_index=True)
    j.columns = ['original', 'new']
    j = j[pd.notnull(j['new'])]

    # Calculate the Norm-1 and return it
    return sum(abs(j['original'] - j['new']))


if __name__ == '__main__':
    """""
    A showcase of our implementation
    """""
    # Start the random walk
    _g = initialize_graph()  # initialize the graph

    init_rand_points = 1  # 1 random initial point
    iterations = int(1e7)  # 10 million iterations per initial point
    print("Starting random walk")
    res = random_walk(_g, init_rand_points, iterations, "rw")  # initialize the graph generic random walk
    write_to_csv("../../data/results/final_random_walk.csv", res)
    random_walk_with_node_removal(_g, init_rand_points, iterations, "rw", res)

    # Start the generalized random walk
    _g = initialize_graph()  # initialize the graph

    init_rand_points = 1000  # 1000 random initial points
    iterations = int(1e4)  # 10 thousand
    print("Starting generalized random walk")
    res = random_walk(_g, init_rand_points, iterations, "grw")  # initialize the graph generic random walk
    write_to_csv("../../data/results/final_generalized_random_walk.csv", res)
    random_walk_with_node_removal(_g, init_rand_points, iterations, "grw", res)
