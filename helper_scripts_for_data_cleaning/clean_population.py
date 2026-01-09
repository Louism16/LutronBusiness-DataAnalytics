import pandas as pd

def load_population_data(file_path, year):
    df = pd.read_csv(file_path, low_memory=False)
    df['ZIP'] = df['NAME'].str.extract(r'ZCTA5 (\d{5})')
    df_clean = df[['ZIP', 'DP05_0001E']].copy()
    df_clean = df_clean.dropna(subset=['ZIP', 'DP05_0001E'])
    df_clean = df_clean.rename(columns={'DP05_0001E': 'population'})
    df_clean['population'] = pd.to_numeric(df_clean['population'], errors='coerce')
    df_clean = df_clean.dropna(subset=['population'])
    df_clean['year'] = year
    return df_clean

def process_population_data():
    file_paths = {
        '2020': 'DownloadedData/ACSDP5Y2020.DP05-Data.csv',
        '2021': 'DownloadedData/ACSDP5Y2021.DP05-Data.csv',
        '2022': 'DownloadedData/ACSDP5Y2022.DP05-Data.csv'
    }
    population_data = [load_population_data(path, year) for year, path in file_paths.items()]
    df_all_years = pd.concat(population_data)
    df_all_years.to_csv('CleanedDataCSVs/population_cleaned.csv', index=False)
    df_pivot = df_all_years.pivot(index='ZIP', columns='year', values='population').reset_index()
    df_pivot['population_growth'] = df_pivot['2022'] - df_pivot['2020']
    df_pivot.to_csv('CleanedDataCSVs/populationGrowth_cleaned.csv', index=False)

if __name__ == "__main__":
    process_population_data()