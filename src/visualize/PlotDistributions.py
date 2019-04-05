import collections
import matplotlib.pyplot as plt
import numpy as np
import csv

with open('../../data/results/lcs_random_walk.csv', 'r', encoding='utf8') as csvfile:
    read_csv = csv.reader(csvfile, delimiter=',')
    product_list = []
    first = True
    for row in read_csv:
        if first:  # Skipping file headers
            first = False
            continue
        print(row[0], row[1])

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