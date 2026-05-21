import pandas as pd
from pathlib import Path


def convert_csv_to_json(csv_path, json_path):
    df = pd.read_csv(csv_path)
    Path(json_path).parent.mkdir(parents=True, exist_ok=True)
    df.to_json(json_path, orient='records', indent=4)
    print(f"Converted {csv_path} to {json_path}")


# Define paths
base_path = "/home/maiconkevyn/PycharmProjects/exoplanets_research/"

csv_files = {
    "data/top_habitable_candidates.csv": "frontend/src/data/top_habitable_candidates.json",
    "data/habitable_zone_calculated.csv": "frontend/src/data/habitable_zone_calculated.json",
    "data/outputs/astrobiology_ranked_candidates.csv": "frontend/src/data/astrobiology_ranked_candidates.json",
}

for csv_file, json_file in csv_files.items():
    convert_csv_to_json(base_path + csv_file, base_path + json_file)

print("All specified CSV files converted to JSON.")
