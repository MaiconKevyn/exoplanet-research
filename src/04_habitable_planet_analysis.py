import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the datasets
df_all = pd.read_csv("/home/maiconkevyn/PycharmProjects/exoplanets_research/data/habitable_zone_calculated.csv")
df_habitable = pd.read_csv("/home/maiconkevyn/PycharmProjects/exoplanets_research/data/potentially_habitable_exoplanets.csv")

# Set plot style
sns.set_style("whitegrid")

# --- Checkpoint 4: Analysis and Visualization ---

# Plot 1: Planet Radius vs. Orbital Period
plt.figure(figsize=(12, 8))
sns.scatterplot(data=df_all, x='pl_orbper', y='pl_rade', alpha=0.3, label='All Exoplanets')
sns.scatterplot(data=df_habitable, x='pl_orbper', y='pl_rade', color='red', s=100, label='Potentially Habitable')
plt.title('Planet Radius vs. Orbital Period')
plt.xlabel('Orbital Period (days)')
plt.ylabel('Planet Radius (Earth radii)')
plt.xscale('log')
plt.yscale('log')
plt.legend()
plt.tight_layout()
plt.savefig('/home/maiconkevyn/PycharmProjects/exoplanets_research/reports/figures/habitable_radius_vs_period.png')
plt.close()
print("Plot 1: Radius vs. Period for habitable planets saved.")

# Plot 2: Distribution of Planet Radii
plt.figure(figsize=(12, 8))
sns.histplot(df_all['pl_rade'], bins=50, kde=True, label='All Exoplanets', alpha=0.5)
sns.histplot(df_habitable['pl_rade'], bins=10, kde=True, label='Potentially Habitable', color='red')
plt.title('Distribution of Planet Radii')
plt.xlabel('Planet Radius (Earth radii)')
plt.ylabel('Frequency')
plt.xlim(0, 10) # Zoom in on smaller planets
plt.legend()
plt.tight_layout()
plt.savefig('/home/maiconkevyn/PycharmProjects/exoplanets_research/reports/figures/habitable_planet_radii_distribution.png')
plt.close()
print("Plot 2: Planet radii distribution for habitable planets saved.")

# Plot 3: Distribution of Stellar Effective Temperatures
plt.figure(figsize=(12, 8))
sns.histplot(df_all['st_teff'], bins=50, kde=True, label='All Exoplanets', alpha=0.5)
sns.histplot(df_habitable['st_teff'], bins=10, kde=True, label='Potentially Habitable', color='red')
plt.title('Distribution of Stellar Effective Temperatures')
plt.xlabel('Stellar Effective Temperature (K)')
plt.ylabel('Frequency')
plt.legend()
plt.tight_layout()
plt.savefig('/home/maiconkevyn/PycharmProjects/exoplanets_research/reports/figures/habitable_stellar_temp_distribution.png')
plt.close()
print("Plot 3: Stellar temperature distribution for habitable planets saved.")

print("\nCheckpoint 4 Complete: Analysis and visualizations are done.")
