
import pandas as pd

# Load the data for potentially habitable exoplanets
df = pd.read_csv("/home/maiconkevyn/PycharmProjects/exoplanets_research/data/potentially_habitable_exoplanets.csv")

# --- Checkpoint 5: Developing a Habitability Score ---

# Function to calculate a simple habitability score
def calculate_habitability_score(row):
    score = 0

    # 1. Planet Size (favoring rocky planets)
    if 0.5 <= row['pl_rade'] <= 1.5:
        score += 1
    elif 1.5 < row['pl_rade'] <= 2.5:
        score += 0.5 # Could be a mini-Neptune, less ideal

    # 2. Stellar Type (favoring Sun-like stars)
    # G-type stars (like our Sun) have temperatures between 5200 K and 6000 K
    if 5200 <= row['st_teff'] <= 6000:
        score += 1
    # K-type stars are also good candidates
    elif 3700 <= row['st_teff'] < 5200:
        score += 0.75
    # M-type stars are common but have issues like tidal locking and stellar flares
    elif 2400 <= row['st_teff'] < 3700:
        score += 0.25

    # 3. Position in the Habitable Zone (already filtered, but we can add nuance)
    # For simplicity, we assume all are equally well-positioned for now
    # but this could be refined to favor the center of the HZ.

    return score

# Calculate the habitability score for each planet
df['habitability_score'] = df.apply(calculate_habitability_score, axis=1)

# Sort the planets by the habitability score
df_ranked = df.sort_values(by='habitability_score', ascending=False)

# Save the ranked list of candidates
output_path = "/home/maiconkevyn/PycharmProjects/exoplanets_research/data/top_habitable_candidates.csv"
df_ranked.to_csv(output_path, index=False)

print("Checkpoint 5 Complete: Habitability score calculated and candidates ranked.")
print("Top 10 most habitable exoplanet candidates:")
print(df_ranked[['pl_name', 'hostname', 'habitability_score', 'pl_rade', 'st_teff']].head(10))
