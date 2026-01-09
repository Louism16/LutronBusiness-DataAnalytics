import pandas as pd
import sys
sys.path.insert(0, './helper_scripts_for_data_merge')
from merge_zillow_realtor import *
from merge_census_data import *

#Begin by reading in the Realtor data and the Zips to County Fips CSV
realtor = pd.read_csv('CleanedDataCSVs/realtor_cleaned.csv')
zip_county = pd.read_csv('CleanedDataCSVs/hudusps_cleaned.csv')

#Merge Realtor and Zips to County Fips by the ZIP column
RealtorZIP_merged = pd.merge(realtor, zip_county, on = "ZIP")

#Read in the Clean Zillow CSV
zillow = pd.read_csv('CleanedDataCSVs/zillow_cleaned.csv')

#Now merge in the Zillow Data with all of the Realtor data by the newly added County Fips column
fullMerged = pd.merge(RealtorZIP_merged, zillow, on = ["county_fips","Date"])

#When merging the Zillow and Realtor Values, you get multiple counties in a ZIP Code so we only keep the county with the highest Zillow Value
fullMerged = remove_dupes(fullMerged)

#Adding a year column that will be used to help merge US Census Data
fullMerged = add_year(fullMerged)

fullMerged.to_csv("CleanedDataCSVs/zillow_realtor_merged.csv", sep=',', index=False, encoding='utf-8')

# Read in the clean CP04 CSV
cp04 = pd.read_csv("CleanedDataCSVs/cp04_cleaned.csv", dtype = {"year": int})

#Merges the State_Cleaned and cp04_cleaned so that we can have the State Abbreviations instead of State Names
cp04 = merge_cp04_states(cp04)

#Merges the cp04 data with the large merged dataset we have built so far
fullMerged = pd.merge(fullMerged, cp04, on = ['year', 'county', 'State'], how = 'left')

#Merges the Cleaned School Data with the rest of the data
school = pd.read_csv("CleanedDataCSVs/school_cleaned.csv", dtype = {"year": int})
fullMerged = pd.merge(fullMerged, school, on = ['year', 'ZIP'], how = 'left')

#Merges the Cleaned Income Data with the rest of the data
income = pd.read_csv("CleanedDataCSVs/income_cleaned.csv", dtype = {"year": int})
fullMerged = pd.merge(fullMerged, income, on = ['year', 'ZIP'], how = 'left')

#Merges the Cleaned Population Data with the rest of the data
population = pd.read_csv("CleanedDataCSVs/population_cleaned.csv", dtype = {"year": int})
fullMerged = pd.merge(fullMerged, population, on = ['year', 'ZIP'], how = 'left')

#Merges in the Cleaned Diversity Data with the rest of the data
diversity = pd.read_csv("CleanedDataCSVs/diversity_cleaned.csv", dtype = {"year": int})
fullMerged = pd.merge(fullMerged, diversity, on = ['year', 'ZIP'], how = 'left')

fullMerged.to_csv("CleanedDataCSVs/FinalData.csv", sep=',', index=False, encoding='utf-8')
print(fullMerged.head())