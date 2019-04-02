import networkx as nx
import Graph

# @TODO: Change into random node set returned (and make a seperate method for constructing the graph)
def random_connected_subgraph(graph, N):
    # Select a random node from the nodelist and add it to the set
    starting_node = Graph.random_node_id(list(graph.nodes))
    print(starting_node)

    current_nodes = set([starting_node])
    outermost_nbs = set([starting_node])
    new_outermost_nbs = set()

    need_more_nodes = True
    while need_more_nodes:
        for n in outermost_nbs:
            # Fetch outgoing edges from this node
            nbs = graph.adj[n]

            # Add all to new neighbours.
            new_outermost_nbs.update(list(nbs))
            # Extend sets
            current_nodes.update(new_outermost_nbs)

            if len(current_nodes) > N:
                need_more_nodes = False
                break

        outermost_nbs = set(new_outermost_nbs)
        if len(outermost_nbs) == 0:
            print("Fully explored connected component")
            break

    # Conststruct subgraph from current_nodes
    return graph.subgraph(list(current_nodes))
