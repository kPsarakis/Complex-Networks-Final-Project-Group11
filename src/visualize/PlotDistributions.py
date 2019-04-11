from pathlib import Path
import collections
import csv
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import graph.Graph as Graph
import seaborn as sns

# This works for MacOS
ROOT_PATH = "../"
# Alternatively for Windows
#ROOT_PATH = "../../"



def read_true_distribution_file():
    filename = ROOT_PATH + "data/processed/products_true_distribution.csv"
    review_scores = []

    with open(filename, 'r') as csvfile:
        csvreader = csv.reader(csvfile, delimiter=";")
        next(csvreader, None)
        for row in csvreader:
            review_scores.append(float(row[2]))

    # Return: list of ratings (normalized)
    count = sum(review_scores)
    return np.array(review_scores) / count


def compute_subsampled_eigenvectors():
    # Load graph
    graph = Graph.initialize_sampled_subgraph()

    # Extract adjacency matrix
    adj_matrix = nx.adjacency_matrix(graph)

    # Compute principal eigenvector
    _, v = np.linalg.eig(adj_matrix)

    # Plot eigenvector as histogram
    plt.hist(v[0], bins='auto')
    plt.show()

def read_subsampled_true_distribution_file():
    filename = ROOT_PATH + "data/processed/sample_true_distribution_counts.csv"
    review_scores = []

    with open(filename, 'r') as csvfile:
        csvreader = csv.reader(csvfile, delimiter=";")
        next(csvreader, None)
        for row in csvreader:
            review_scores.append(float(row[1]))

    # Return: list of ratings (normalized)
    count = sum(review_scores)
    return np.array(review_scores) / count


def read_subsampled_results_file(filename):
    review_scores = []
    with open(ROOT_PATH + filename, 'r') as csvfile:
        csvreader = csv.reader(csvfile, delimiter=",")
        next(csvreader, None)
        for row in csvreader:
            review_scores.append(float(row[1]))

    return np.array(review_scores)


def plot_distribution(dists, filename, title):
    BASE_DIR = ROOT_PATH + "reports/figures/"

    Y_MAX = 25000
    plt.hist(dists, bins=500, density=True, log=True)
    plt.title(title)
    plt.xlabel("Popularity")
    plt.ylim(0, Y_MAX)
    plt.savefig(BASE_DIR + filename)
    plt.close()


def make_histograms():
    # True distribution
    Y_MAX = 25000
    dists = read_true_distribution_file()
    plot_distribution(dists, "dist_true_fullgraph.png", "PDF For full graph")

    # Random walk distribution
    dists = read_subsampled_true_distribution_file()
    plot_distribution(dists, "dist_true_sampled.png", "PDF For subsampled graph")

    dists = read_subsampled_results_file("data/results/final_random_walk.csv")
    plot_distribution(dists, "dist_rw_sampled.png", "PDF For random walk")


    dists = read_subsampled_results_file("data/results/rw_3base.csv")
    plot_distribution(dists, "dist_rw_3base.png", "PDF for removal (base) RW")

    dists = read_subsampled_results_file("data/results/rw_3bot.csv")
    plot_distribution(dists, "dist_rw_3bot.png", "PDF for removal (bot) RW")

    dists = read_subsampled_results_file("data/results/rw_3top.csv")
    plot_distribution(dists, "dist_rw_3top.png", "PDF for removal (top) RW")

    dists = read_subsampled_results_file("data/results/grw_3base.csv")
    plot_distribution(dists, "dist_grw_3base.png", "PDF for removal (base) GRW")

    dists = read_subsampled_results_file("data/results/grw_3bot.csv")
    plot_distribution(dists, "dist_grw_3bot.png", "PDF for removal (bot) GRW")    

    dists = read_subsampled_results_file("data/results/grw_3top.csv")
    plot_distribution(dists, "dist_grw_3top.png", "PDF for removal (top) GRW")

    dists = read_subsampled_results_file("data/results/final_generalized_random_walk.csv")
    plot_distribution(dists, "dist_grw_sampled.png", "PDF for GRW")    

    # Principal eigenvector (as a validation) distribution
    # dists = compute_subsampled_eigenvectors()
    # plt.hist(dists, bins=500)
    # plt.savefig(BASE_DIR + "dist_eigen_subgraph.png")

    # Generalized random walk

if __name__ == '__main__':
    make_histograms()

# test_histogram()

# with open('../../data/results/lcs_random_walk.csv', 'r', encoding='utf8') as csvfile:
#     read_csv = csv.reader(csvfile, delimiter=',')
#     product_list = []
#     first = True
#     for row in read_csv:
#         if first:  # Skipping file headers
#             first = False
#             continue
#         print(row[0], row[1])

def plot_degree_distribution(dd):
    # Explicitly set degrees were no count to zero

    degree_sequence = sorted(dd, reverse=True)  # degree sequence
    degree_count = collections.Counter(degree_sequence)
    degree, count = zip(*degree_count.items())
    prob = [x/sum(count) for x in count]  # Dividing each degree by count to obtain probability)
    # Finding which degree have zero count
    for i in range(degree_sequence[0]):
        if i not in degree:
            degree = list(degree)
            degree.append(i)
            prob = list(prob)
            prob.append(0)
            degree = tuple(degree)
            prob = tuple(prob)
    indexes = np.argsort(degree) # Finding the indexes with which to sort the probability list
    sorted_degree = sorted(degree)
    sorted_prob = []
    # Recreating the probability list with the correct ordering
    for index in indexes:
        sorted_prob.append(prob[index])
    plt.plot(sorted_degree, sorted_prob, 'r')
    plt.title("Degree Distribution")
    plt.ylabel("Pr[D = k]")
    plt.xlabel("Degree")
    plt.show()