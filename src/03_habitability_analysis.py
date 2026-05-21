
import pandas as pd
import numpy as np

# Load the data from Checkpoint 2
df = pd.read_csv("/home/maiconkevyn/PycharmProjects/exoplanets_research/data/habitable_zone_calculated.csv")

# --- Checkpoint 3: Identifying Potentially Habitable Exoplanets ---

# We need the semi-major axis of the planet's orbit to determine its position
# relative to the habitable zone. Let's add it to our required columns.
if 'pl_orbsmax' not in df.columns:
    print("Error: 'pl_orbsmax' (semi-major axis) column is missing.")
else:
    # Function to check if a planet is in the habitable zone
    def check_habitability(row):
        # The semi-major axis (pl_orbsmax) is in AU (Astronomical Units)
        # The habitable zone boundaries are also in AU
        return row['hz_inner'] <= row['pl_orbsmax'] <= row['hz_outer']

    # Apply the function to create the 'is_in_habitable_zone' column
    df['is_in_habitable_zone'] = df.apply(check_habitability, axis=1)

    # Filter for potentially habitable exoplanets
    habitable_planets = df[df['is_in_habitable_zone'] == True]

    # Save the list of potentially habitable exoplanets
    output_path = "/home/maiconkevyn/PycharmProjects/exoplanets_research/data/potentially_habitable_exoplanets.csv"
    habitable_planets.to_csv(output_path, index=False)

    print("Checkpoint 3 Complete: Potentially habitable exoplanets identified.")
    print(f"Number of potentially habitable exoplanets found: {len(habitable_planets)}")
    print("Details of the first 5 potentially habitable exoplanets:")
    print(habitable_planets.head())
