import kagglehub
import os
import pandas as pd

path = kagglehub.dataset_download("myrios/cost-of-living-index-by-country-by-number-2024")

for f in os.listdir(path):
    if f.endswith(".csv"):
        df = pd.read_csv(os.path.join(path, f))
        matches = df[df["Country"].str.contains("India", case=False, na=False)]
        print("Matches found for 'India':")
        print(matches)
        print("\nTotal countries in dataset:", len(df))