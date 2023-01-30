import csv
import os

diamonds_df  = "diamonds.csv"




# def save_new_csv():
#     with open(diamonds_df) as inp, open("diamonds_df_id", 'w') as out:
#         reader = csv.reader(inp)
#         writer = csv.writer(out, delimiter=',')
#         #No need to use `insert(), `append()` simply use `+` to concatenate two lists.
#         writer.writerow(['id'] + next(reader))
#         #Iterate over enumerate object of reader and pass the starting index as 1.
#         writer.writerows([i] + row for i, row in enumerate(reader, 1))

# save_new_csv()

def save_csv(data): # data is a list of dictionaries
    with open(diamonds_df , 'w', newline='') as file:
        # set the headers of the csv file
        fieldnames = data[0].keys() # make the keys of the first dictionary in the list "data"
        writer = csv.DictWriter(file, fieldnames=fieldnames) #  module that allows to write dictionaries to a CSV file
        writer.writeheader() #  writes the headers csv file - the keys of the first dictionary in the list.
        for row in data:
            writer.writerow(row) # Each row - dictionary will be written csv file with the keys as the headers.

# def add_toCSV(OBJ):

    


def load_csv():
    data = []
    with open(diamonds_df , 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            data.append(row)
    return data