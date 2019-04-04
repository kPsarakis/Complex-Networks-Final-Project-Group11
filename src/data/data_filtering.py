import csv
import string

with open('../../data/interim/amazon-meta_extracted.csv', encoding='utf8', mode='w', newline='') as data_file:
    data_writer = csv.writer(data_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    data_writer.writerow(['Product_id', 'Product_title', 'Final_year_review_count', 'Total_review_count', 'Average_rating', 'Product_recommendations'])

with open('../../data/raw/amazon-meta.txt', 'r', encoding='utf8') as f:
    for j in range(0, 3):
        f.readline()  # Skipping the first three file lines
    fields = 0  # Data fields collected
    year_dict = {}  # Review year dictionary (year, count)
    total_review_count = 0  # Total number of reviews in total:
    reviews = 0  # Total number of review rows
    line = f.readline()
    while line:
        if 'ASIN:' in line:
            fields += 1  # Data field collected
            prod_id = line.split(' ')[-1][:-1]  # Splitting with space and removing new line
        if 'discontinued product' in line:
            fields = 0  # Skipping discontinued products
            total_review_count = 0
        if 'title:' in line:
            fields += 1
            title = line.split(' ', 3)[-1][:-1]  # Extracting the tile and removing new line
            title = title.translate(str.maketrans(string.punctuation, ' '*len(string.punctuation)))  # replacing punctuation with spaces to have no issues with the delimeter
            title = ' '.join(title.split())  # removing multiple whitespaces
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
            total_review_count = substring[1]  # Extracting the review count
            avg_rating = substring[-1][:-1]  # Extracting the avg rating and removing new line
        line = f.readline()
        while line.startswith('    '):  # if line starts with four whitespaces (only reviews and product categories have that)
            fields += 1
            reviews += 1
            year = line.split(' ')[4][:4]
            if year in year_dict:
                year_dict[year] += 1
            else:
                year_dict[year] = 1
            line = f.readline()

        if fields == reviews + 5:
            if len(year_dict) > 1:
                max_year = 0
                for key, value in year_dict.items():
                    if int(key) > max_year:
                        max_year = int(key)
                        review_count = value
                with open('../../data/interim/amazon-meta_extracted.csv', encoding='utf8', mode='a', newline='') as data_file:
                    data_writer = csv.writer(data_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                    data_writer.writerow([prod_id, title, review_count, total_review_count, avg_rating, similar])
            # Reset counters for new product
            fields = 0
            total_review_count = 0
            reviews = 0
            year_dict = {}
