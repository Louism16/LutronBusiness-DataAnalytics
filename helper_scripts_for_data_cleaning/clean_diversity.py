import pandas as pd

def calculate_diversity_index(file_path, year):
    df = pd.read_csv(file_path, low_memory=False)
    df_race = df[['NAME', 'DP05_0037PE', 'DP05_0038PE', 'DP05_0039PE', 'DP05_0040PE', 'DP05_0035PE']].copy()
    df_race.columns = ['ZIP', 'White', 'Black', 'American Indian', 'Asian', 'Two or More Races']
    df_race['ZIP'] = df_race['ZIP'].str.extract(r'ZCTA5 (\d{5})')
    df_race = df_race.dropna()
    race_columns = ['White', 'Black', 'American Indian', 'Asian', 'Two or More Races']
    df_race[race_columns] = df_race[race_columns].apply(pd.to_numeric, errors='coerce')
    df_race['simpson_diversity_index'] = 1 - (df_race[race_columns] / 100).pow(2).sum(axis=1)
    df_race['year'] = year
    return df_race[['ZIP', 'simpson_diversity_index', 'year']]

def process_diversity_data():
    file_paths = {
        '2020': 'DownloadedData/ACSDP5Y2020.DP05-Data.csv',
        '2021': 'DownloadedData/ACSDP5Y2021.DP05-Data.csv',
        '2022': 'DownloadedData/ACSDP5Y2022.DP05-Data.csv'
    }
    diversity_data = [calculate_diversity_index(path, year) for year, path in file_paths.items()]
    df_all_years = pd.concat(diversity_data)
    df_all_years.to_csv('CleanedDataCSVs/diversity_cleaned.csv', index=False)
    df_pivot = df_all_years.pivot(index='ZIP', columns='year', values='simpson_diversity_index').reset_index()
    df_pivot['diversity_growth_metric'] = pd.cut(
        df_pivot['2022'] - df_pivot['2020'],
        bins=[-float('inf'), -0.1, 0, 0.1, 0.2, float('inf')],
        labels=[1, 2, 3, 4, 5]
    )
    df_pivot.to_csv('CleanedDataCSVs/diversityGrowth_cleaned.csv', index=False)

if __name__ == "__main__":
    process_diversity_data()