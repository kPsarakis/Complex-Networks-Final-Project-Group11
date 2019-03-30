import csv

with open('../../data/interim/amazon-meta_extracted.csv', encoding='utf8', mode='a', newline='') as data_file:
    data_writer = csv.writer(data_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    data_writer.writerow(['Product id', 'Product title', 'Product review count', 'Product average rating', 'Product recommendations'])

with open('../../data/raw/amazon-meta.txt', 'r', encoding='utf8') as f:
    lines = 0
    for line in f:
        lines += 1  # Calculating the number of lines in the file
    fields = 0  # Data fields collected
    f.seek(0)  # Go to start of file again
    for j in range(0, 3):
        f.readline()  # Skipping the first three file lines
    for i in range(4, lines+1):
        line = f.readline()
        if 'ASIN:' in line:
            fields += 1  # Data field collected
            prod_id = line.split(' ')[-1][:-1]  # Splitting with space and removing new line
        if 'discontinued product' in line:
            fields = 0  # Skipping discontinued products
        if 'title:' in line:
            fields += 1
            title = line.split(' ', 3)[-1][:-1]  # Extracting the tile and removing new line
        if 'similar:' in line:
            fields += 1
            if len(list(filter(None, line.split(' ')))) == 2:  # Checking if the product has recommendations
                similar = 0
            else:
                similar = list(filter(None, line.split(' ')))[2:]  # Splitting with space, removing empty entries and taking the ASINs
                similar[len(similar) - 1] = similar[len(similar)-1][:-1]  # removing new line
        if 'reviews:' in line:
            fields += 2
            substring = list(filter(None,line.split(' ', 3)[-1].split(' '))) # Extracting text from "total:" till the end of the line
            review_count = substring[1]  # Extracting the review count
            avg_rating = substring[-1][:-1]  # Extracting the avg rating and removing new line
        if fields == 5:
            fields = 0  # start collecting info for new product
            with open('../../data/interim/amazon-meta_extracted.csv', encoding='utf8', mode='a', newline='') as data_file:
                data_writer = csv.writer(data_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                data_writer.writerow([prod_id, title, review_count, avg_rating, similar])
