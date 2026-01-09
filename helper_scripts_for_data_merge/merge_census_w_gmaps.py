import pandas as pd

def merge_data():
    # File paths
    population_file = 'LutronHousingDA/CleanedDataCSVs/populationGrowth_cleaned.csv'
    diversity_file = 'LutronHousingDA/CleanedDataCSVs/diversityGrowth_cleaned.csv'
    google_maps_file = 'LutronHousingDA/CleanedDataCSVs/googleMapsAPI_cleaned.csv'
    
    # Load the CSV files into DataFrames
    population_df = pd.read_csv(population_file)
    diversity_df = pd.read_csv(diversity_file)
    google_maps_df = pd.read_csv(google_maps_file)
    
    # Merge population and diversity data on 'ZIP Code'
    merged_df = pd.merge(population_df, diversity_df, on='ZIP Code', how='inner')
    
    # Merge with Google Maps data on 'Zipcode'
    final_merged_df = pd.merge(google_maps_df, merged_df, left_on='Zipcode', right_on='ZIP Code', how='inner')
    
    # Drop duplicate 'ZIP Code' column
    final_merged_df.drop(columns=['ZIP Code'], inplace=True)
    
    # Save the merged DataFrame to a new CSV file
    output_file_path = 'LutronHousingDA/CleanedDataCSVs/Merged_Population_Diversity_GoogleMaps.csv'
    final_merged_df.to_csv(output_file_path, index=False)
    
    print(f"Merged data saved to: {output_file_path}")

if __name__ == "__main__":
    merge_data()