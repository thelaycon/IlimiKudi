import os
import pandas as pd

# Define the directory containing the CSV files
directory = 'datasets'

# Get all CSV files in the directory
csv_files = [f for f in os.listdir(directory) if f.endswith('.csv')]

# Initialize an empty list to store dataframes
dataframes = []

# Read each CSV file and append its dataframe to the list (excluding headers after the first file)
for i, file in enumerate(csv_files):
    file_path = os.path.join(directory, file)
    if i == 0:
        # Read the first file (with header)
        df = pd.read_csv(file_path)
    else:
        # Read subsequent files (without header)
        df = pd.read_csv(file_path, header=0)
    
    dataframes.append(df)

# Concatenate all dataframes into a single dataframe
merged_df = pd.concat(dataframes, ignore_index=True)

# Save the merged dataframe to a new CSV file in the same directory
merged_file_path = os.path.join(directory, 'merged.csv')
merged_df.to_csv(merged_file_path, index=False)

print(f'Merged CSV saved as {merged_file_path}')
