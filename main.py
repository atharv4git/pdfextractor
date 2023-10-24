import camelot
import json

# scans the pdf file for tables
tables = camelot.read_pdf("./AR_2022_23.pdf", pages="200", flavour="lattice")


# Initialize a dictionary to store JSON representations of tables
tables_json = {}

# Convert each table to JSON
for i, table in enumerate(tables):
    # Get the table data as a Pandas DataFrame
    table_data = table.df
    
    # Convert the DataFrame to a JSON object with 'records' orientation
    table_json = table_data.to_json(orient='records')
    
    # Create a key for each table, e.g., 'table1', 'table2', etc.
    table_key = f'table{i+1}'
    
    # Add the JSON object to the dictionary using the table_key
    tables_json[table_key] = json.loads(table_json)

json_file_path = 'tables_data.json'

# Save the dictionary as a JSON file
with open(json_file_path, 'w') as json_file:
    json.dump(tables_json, json_file)

# Confirm that the JSON file has been saved
print(f"JSON data saved to {json_file_path}")