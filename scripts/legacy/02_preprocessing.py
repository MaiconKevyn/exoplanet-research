import pandas as pd
import numpy as np

# Load the processed data
df = pd.read_parquet("/home/maiconkevyn/PycharmProjects/exoplanets_research/data/processed_exoplanet_data.parquet")

# --- Data Cleaning ---

# 1. Address mixed-type columns (from DtypeWarning)
# Convert columns to string type, filling NaNs with a placeholder
for col in ['hd_name', 'hip_name']:
    if col in df.columns:
        df[col] = df[col].astype(str).replace('nan', np.nan)

# 2. Handle missing values
# Calculate missing percentage, but exclude key columns from being dropped
missing_percentage = df.isnull().sum() / len(df)
key_cols = ['pl_masse', 'pl_rade']
cols_to_drop = missing_percentage[(missing_percentage > 0.5) & (~missing_percentage.index.isin(key_cols))].index
df_cleaned = df.drop(columns=cols_to_drop)

print(f"Dropped {len(cols_to_drop)} columns with more than 50% missing values.")

# Impute missing values for key columns with the median
for col in key_cols:
    if col in df_cleaned.columns:
        median_val = df_cleaned[col].median()
        df_cleaned[col].fillna(median_val, inplace=True)
        print(f"Filled missing values in '{col}' with median value: {median_val:.2f}")

# --- Feature Engineering ---

# 1. Classify Planet Type
def classify_planet(row):
    # Mass is in Earth masses (pl_masse), radius is in Earth radii (pl_rade)
    mass = row['pl_masse']
    radius = row['pl_rade']

    if pd.isna(mass) or pd.isna(radius):
        return 'Unknown'

    if mass > 10 and radius > 4:
        return 'Gas Giant'
    elif mass > 10 and radius <= 4:
        return 'Neptunian'
    elif 1 < mass <= 10:
        return 'Super-Earth'
    elif mass <= 1:
        return 'Terrestrial'
    else:
        return 'Unknown'

if 'pl_masse' in df_cleaned.columns and 'pl_rade' in df_cleaned.columns:
    df_cleaned['planet_type'] = df_cleaned.apply(classify_planet, axis=1)
    print("\nPlanet type classification:")
    print(df_cleaned['planet_type'].value_counts())

# Save the preprocessed data
df_cleaned.to_parquet("/home/maiconkevyn/PycharmProjects/exoplanets_research/data/preprocessed_exoplanet_data.parquet")
print("\nPreprocessed data saved to data/preprocessed_exoplanet_data.parquet")