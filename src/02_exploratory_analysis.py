import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the processed data
df = pd.read_csv("/home/maiconkevyn/PycharmProjects/exoplanets_research/data/processed_exoplanet_data.csv")

# Set the style for the plots
sns.set_style("whitegrid")

# --- Plot 1: Distribution of Exoplanet Discovery Methods ---
plt.figure(figsize=(12, 8))
sns.countplot(y=df['discoverymethod'], order=df['discoverymethod'].value_counts().index, palette='viridis')
plt.title('Distribution of Exoplanet Discovery Methods')
plt.xlabel('Number of Exoplanets')
plt.ylabel('Discovery Method')
plt.tight_layout()
plt.savefig('/home/maiconkevyn/PycharmProjects/exoplanets_research/reports/figures/discovery_methods.png')
plt.close()

print("Plot 1: Distribution of discovery methods saved.")

# --- Plot 2: Distribution of Exoplanets by Discovery Year ---
plt.figure(figsize=(12, 8))
sns.histplot(df['disc_year'], bins=30, kde=True, color='royalblue')
plt.title('Distribution of Exoplanets by Discovery Year')
plt.xlabel('Discovery Year')
plt.ylabel('Number of Exoplanets')
plt.tight_layout()
plt.savefig('/home/maiconkevyn/PycharmProjects/exoplanets_research/reports/figures/discovery_year.png')
plt.close()

print("Plot 2: Distribution of discovery years saved.")

# --- Plot 3: Relationship between Planet Mass and Radius ---
plt.figure(figsize=(12, 8))
sns.scatterplot(data=df, x='pl_masse', y='pl_rade', alpha=0.5, color='coral')
plt.title('Planet Mass vs. Radius (Earth units)')
plt.xlabel('Planet Mass (Earth mass)')
plt.ylabel('Planet Radius (Earth radius)')
plt.xscale('log')
plt.yscale('log')
plt.tight_layout()
plt.savefig('/home/maiconkevyn/PycharmProjects/exoplanets_research/reports/figures/mass_vs_radius.png')
plt.close()

print("Plot 3: Mass vs. Radius plot saved.")

# --- Plot 4: Distribution of Stellar Effective Temperature ---
plt.figure(figsize=(12, 8))
sns.histplot(df['st_teff'], bins=40, kde=True, color='firebrick')
plt.title('Distribution of Stellar Effective Temperature')
plt.xlabel('Stellar Effective Temperature (K)')
plt.ylabel('Number of Stars')
plt.tight_layout()
plt.savefig('/home/maiconkevyn/PycharmProjects/exoplanets_research/reports/figures/stellar_temperature.png')
plt.close()

print("Plot 4: Stellar temperature distribution saved.")

# --- Plot 5: Orbital Period vs. Planet Mass ---
plt.figure(figsize=(12, 8))
sns.scatterplot(data=df, x='pl_orbper', y='pl_masse', alpha=0.5, color='purple')
plt.title('Orbital Period vs. Planet Mass')
plt.xlabel('Orbital Period (days)')
plt.ylabel('Planet Mass (Earth mass)')
plt.xscale('log')
plt.yscale('log')
plt.tight_layout()
plt.savefig('/home/maiconkevyn/PycharmProjects/exoplanets_research/reports/figures/period_vs_mass.png')
plt.close()

print("Plot 5: Orbital period vs. mass plot saved.")

print("\nAll plots have been generated and saved in the 'reports/figures' directory.")