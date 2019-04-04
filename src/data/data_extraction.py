import csv
import ast

# Writing file headlines
with open('../../data/processed/products_true_distribution.csv', encoding='utf8', mode='w', newline='') as product_file:
    product_writer = csv.writer(product_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    product_writer.writerow(['Product_id', 'Product_title', 'Final_year_review_count', 'Total_review_count', 'Average_rating'])

with open('../../data/processed/products_nodes_links.csv', encoding='utf8', mode='w', newline='') as network_file:
                network_writer = csv.writer(network_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                network_writer.writerow(['Node1', 'Node2'])

with open('../../data/interim/amazon-meta_extracted.csv', 'r', encoding='utf8') as csvfile:
    read_csv = csv.reader(csvfile, delimiter=',')
    product_list = []
    first = True
    for row in read_csv:
        if first:  # Skipping file headers
            first = False
            continue
        # Output true distribution data
        with open('../../data/processed/products_true_distribution.csv', encoding='utf8', mode='a',
                  newline='') as product_file:
            product_writer = csv.writer(product_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            product_writer.writerow([row[0], row[1], row[2], row[3], row[4]])
        # Check if the product has recommendations
        if row[5] != "0":
            recommendations = ast.literal_eval(row[5])  # Converting list formatted as string back into list
            # For every recommendation of a product
            for recommendation in recommendations:
                with open('../../data/processed/products_nodes_links.csv', encoding='utf8', mode='a',
                          newline='') as network_file:
                    network_writer = csv.writer(network_file, delimiter=',', quotechar='"',
                                                quoting=csv.QUOTE_MINIMAL)
                    network_writer.writerow([row[0], recommendation])
