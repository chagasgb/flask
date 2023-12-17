import csv
import json

csv_file_path = 'sample.csv'
json_file_path = 'sample.json'

data = []

with open(csv_file_path, 'r') as csv_file:
    csv_reader = csv.DictReader(csv_file)
    for row in csv_reader:
        data.append(row)

with open(json_file_path, 'w') as json_file:
    json.dump(data, json_file, indent=4)

print(f'O arquivo {csv_file_path} foi convertido para JSON em {json_file_path}.')