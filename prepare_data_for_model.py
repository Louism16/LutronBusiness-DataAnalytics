import pandas as pd
import sys
sys.path.insert(0, './helper_scripts_for_data_prep')
from merge_census_data import *
from merge_lutron_data import *

# Reading in the merged Zillow and Realtor data
fullMerged = pd.read_csv("CleanedDataCSVs/zillow_realtor_merged.csv")

# Splitting the merged real estate data by year, taking the three most recent years
years = split_data_by_year_monthly(fullMerged)

# Merging in the CP04 data for each of the three years
years = merge_in_cp04(years)

# Merging in the school enrollment data for each of the three years
years = merge_in_school(years)

# Merging in the income data for each of the three years
years = merge_in_income(years)

# Merging in the population data for each of the three years
years = merge_in_population(years)

# Merging in the diversity data for each of the three years
years = merge_in_diversity(years)

# Reading in the CSV with the Lutron data
lutron = pd.read_csv("DownloadedData/LutronData.csv")

# Cleans the Lutron data in preparation for merging
lutron = clean_lutron_data(lutron)

# Split the Lutron data by year and merge it with the rest of the data for each year
years = split_and_merge(lutron, years, True)

# Aggregate values of multiple zip codes in each city for each year of data
years[0] = aggregate_zips(years[0])
years[1] = aggregate_zips(years[1])
years[2] = aggregate_zips(years[2])

# Concatenating each year of data together
modelData = pd.concat([years[0], years[1], years[2]])

# Saving the final merged data set to CleanedDataCSVs
modelData.to_csv("CleanedDataCSVs/cleaned_model_data.csv", sep=',', index=False, encoding='utf-8')