import os
import pandas as pd

# Directory containing the .txt files
directory = 'output_data'

# Initialize an empty list to store data
data = []

# Iterate over all files in the directory
for filename in os.listdir(directory):
    if filename.endswith(".txt"):
        # Extract the DBNLti_id from the filename (assuming filename is the ID)
        DBNLti_id = filename.split('.')[0]

        # Full file path
        file_path = os.path.join(directory, filename)

        # Read the file content
        with open(file_path, 'r', encoding='utf-8') as file:
            lines = file.readlines()

            # Extract header and values
            header = lines[0].strip().split('\t')
            values = lines[1].strip().split('\t')

            # Append the DBNLti_id to the values
            values.insert(0, DBNLti_id)

            # Append to the data list
            data.append(values)

# Create a DataFrame from the collected data
df = pd.DataFrame(data, columns=['DBNLti_id'] + header)

# Save the DataFrame to a .tsv file
df.to_csv('output.tsv', sep='\t', index=False)

print("TSV file has been created successfully.")
