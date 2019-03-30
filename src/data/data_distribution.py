import csv
import random

# Writing file headlines
# with open('../../data/processed/products_true_distribution.csv', encoding='utf8', mode='w', newline='') as product_file:
#     product_writer = csv.writer(product_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
#     product_writer.writerow(['Product id', 'Product title', 'Product review count', 'Product average rating'])
#
# with open('../../data/processed/products_nodes_links.csv', encoding='utf8', mode='w', newline='') as network_file:
#                 network_writer = csv.writer(network_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
#                 network_writer.writerow(['Node 1', 'Node 2'])

with open('../../data/interim/amazon-meta_extracted.csv', 'r', encoding='utf8') as csvfile:
    read_csv = csv.reader(csvfile, delimiter=',')
    for row in read_csv:
        print(row)
        # append all items to list and random sample
    # random.sample(product_list, 10000)
