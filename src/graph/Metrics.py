import networkx as nx


def print_metrics(g: nx.Graph):

    # Number of nodes
    n = g.number_of_nodes()
    print("Number of nodes: ", n)

    # Number of links
    li = g.number_of_edges()
    print("Number of links: ", li)

    # Link density
    p = nx.density(g)
    print("Link density: ", p)

    # Average degree
    print("Average degree: ", 2*li/n)

    # Degree variance
    print("Degree variance: ", get_degree_variance(g))

    # Plot degree distribution
    plot_degree_distribution(dict(g.degree).values())

    # Degree correlation (assortativity)
    r = nx.degree_assortativity_coefficient(g)
    print("Degree correlation (assortativity): ", r)

    # Clustering coeffcient
    c = nx.average_clustering(g)
    print("Clustering coeffcient: ", c)

    # Average hop count
    eh = nx.average_shortest_path_length(g)
    print("Average hop count: ", eh)

    # Diameter (Hmax)
    hmax = get_max_hop_count(dict(nx.shortest_path_length(g)).values())
    print("Diameter (Hmax): ", hmax)

    # Spectral radius of the adjacency matrix
    lambda1 = max(nx.adjacency_spectrum(g))
    print("Spectral radius of the adjacency matrix: ", lambda1)

    # Algebraic connectivity
    ac = nx.algebraic_connectivity(g)
    print("Algebraic connectivity: ", ac)


# Calculate the average degree of a Graph
def get_average_degree(g):

    n = g.number_of_nodes()
    s = 0

    for i in range(1, n + 1):
        s += g.degree(i)

    return s / n


# Calculate the degree variance of a Graph
def get_degree_variance(g):

    n = g.number_of_nodes()
    m = get_average_degree(g)
    s = 0

    for i in range(1, n + 1):
        s += (g.degree(i)-m)**2

    return s / n


# Plot degree distribution
def plot_degree_distribution(dd):

    import collections
    import matplotlib.pyplot as plt
    import numpy as np
    # Explicitly set degrees were no count to zero

    degree_sequence = sorted(dd, reverse=True)  # degree sequence
    degree_count = collections.Counter(degree_sequence)
    degree, count = zip(*degree_count.items())
    prob = [x/sum(count) for x in count]  # Dividing each degree by count to obtain probability)
    # Finding which degree have zero count
    for i in range(139):
        if i not in degree:
            degree = list(degree)
            degree.append(i)
            prob = list(prob)
            prob.append(0)
            degree = tuple(degree)
            prob = tuple(prob)
    indexes = np.argsort(degree)  # Finding the indexes with which to sort the probability list
    sortedDegree = sorted(degree)
    sortedProb = []
    # Recreating the probability list with the correct ordering
    for index in indexes:
        sortedProb.append(prob[index])
    # plt.plot(degree, prob)
    plt.plot(sortedDegree, sortedProb, 'r')
    plt.title("Degree Distribution")
    plt.ylabel("Pr[D = k]")
    plt.xlabel("Degree")
    plt.show()


# Max Hop-Count (diameter)
def get_max_hop_count(sp):

    _max = -1

    for v in sp:

        t_max = max(v.values())

        if _max < t_max:
            _max = t_max

    return _max
