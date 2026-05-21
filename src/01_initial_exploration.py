

import pandas as pd

# Define the path to the data file
file_path = "/home/maiconkevyn/PycharmProjects/exoplanets_research/data/PS_2025.06.22_09.41.26.csv"

# Function to generate a data dictionary
def generate_data_dictionary(df):
    data_dict = {
        'Column': [],
        'DataType': [],
        'NonNullCount': [],
        'NullCount': [],
        'UniqueValues': []
    }
    for col in df.columns:
        data_dict['Column'].append(col)
        data_dict['DataType'].append(df[col].dtype)
        data_dict['NonNullCount'].append(df[col].count())
        data_dict['NullCount'].append(df[col].isnull().sum())
        data_dict['UniqueValues'].append(df[col].nunique())
    return pd.DataFrame(data_dict)

# Read the CSV, skipping the initial comment lines
try:
    # Skipping 294 comment lines and then reading the header
    df = pd.read_csv(file_path, on_bad_lines='skip', skiprows=294)
    
    print("First 5 rows of the dataset:")
    print(df.head())
    
    print("\nColumn names:")
    print(df.columns.tolist())

    # Generate and print the data dictionary
    data_dictionary = generate_data_dictionary(df)
    print("\nData Dictionary:")
    print(data_dictionary)

    # Save the data dictionary to a file
    data_dictionary.to_csv("/home/maiconkevyn/PycharmProjects/exoplanets_research/data/data_dictionary.csv", index=False)
    print("\nData dictionary saved to data/data_dictionary.csv")

    # Save the cleaned data to a CSV file
    df.to_csv("/home/maiconkevyn/PycharmProjects/exoplanets_research/data/processed_exoplanet_data.csv", index=False)
    print("\nProcessed data saved to data/processed_exoplanet_data.csv")

except FileNotFoundError:
    print(f"Error: The file was not found at {file_path}")
except Exception as e:
    print(f"An error occurred: {e}")

