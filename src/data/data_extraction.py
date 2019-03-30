import csv
import random
import ast

# Writing file headlines
with open('../../data/processed/products_true_distribution.csv', encoding='utf8', mode='w', newline='') as product_file:
    product_writer = csv.writer(product_file, delimiter='#', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    product_writer.writerow(['Product id', 'Product title', 'Product review count', 'Product average rating'])

with open('../../data/processed/products_nodes_links.csv', encoding='utf8', mode='w', newline='') as network_file:
                network_writer = csv.writer(network_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                network_writer.writerow(['Node 1', 'Node 2'])

with open('../../data/interim/amazon-meta_extracted.csv', 'r', encoding='utf8') as csvfile:
    read_csv = csv.reader(csvfile, delimiter=',')
    product_list = []
    first = True
    for row in read_csv:
        if first:  # Skipping file headers
            first = False
            continue
        product_list.append(row)
    # random_selection = random.sample(product_list, 10000)
    for product in product_list:
        # Output true distribution data delimeted with # to not mix with commas in the title
        with open('../../data/processed/products_true_distribution.csv', encoding='utf8', mode='a',
                  newline='') as product_file:
            product_writer = csv.writer(product_file, delimiter='#', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            product_writer.writerow([product[0], product[1], product[2], product[3]])
        # Check if the product has recommendations
        if product[4] != "0":
            recommendations = ast.literal_eval(product[4])  # Converting list formatted as string back into list
            # For every recommendation of a product
            for recommendation in recommendations:
                with open('../../data/processed/products_nodes_links.csv', encoding='utf8', mode='a',
                          newline='') as network_file:
                    network_writer = csv.writer(network_file, delimiter=',', quotechar='"',
                                                quoting=csv.QUOTE_MINIMAL)
                    network_writer.writerow([product[0], recommendation])