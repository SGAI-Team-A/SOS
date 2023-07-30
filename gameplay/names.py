import random
import csv
import os

def get_random_name(name_path):
    with open(name_path, 'r', newline='') as csvfile:
        csv_reader = csv.reader(csvfile)
        names_list = list(csv_reader)

    if not names_list:
        raise ValueError(f"The file {name_path} is empty.")

    random_name = random.choice(names_list)[0].strip()
    return random_name

def generate_name(gender):
    fp = ""
    if gender == "woman":
        fp = "fem_names.csv"
    else:
        fp = "masc_names.csv"

    last_name_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'name_data', 'last_names.csv')
    name_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'name_data', fp)
    return f"{get_random_name(name_path)} {get_random_name(last_name_path)}"
