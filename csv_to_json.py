import csv
import json

csv_file_path = 'sample.csv'
json_file_path = 'sample.json'

data = []

def converter_para_float(valor):
    try:
        return float(valor)
    except ValueError:
        return valor

with open(csv_file_path, 'r') as csv_file:
    csv_reader = csv.DictReader(csv_file)
    for row in csv_reader:
        # Transforme todos os campos em float, se possível
        row = {key: converter_para_float(value) for key, value in row.items()}
        data.append(row)

with open(json_file_path, 'w') as json_file:
    json.dump(data, json_file, indent=4)

print(f'O arquivo {csv_file_path} foi convertido para JSON em {json_file_path}.')
