import pandas as pd
import time
import sys
sys.path.insert(0, './helper_scripts_for_data_cleaning')
from clean_zillow import *
from clean_realtor import *
from clean_cp04 import *
from clean_school import *
from clean_income import *
from clean_population import *
from clean_diversity import *
from clean_googleMapsAPI import *

start = time.perf_counter()
last = start

pd.set_option('display.max_columns', None)

def end_timer(msg):
	global last
	end = time.perf_counter()
	print(f"{msg} {end - last:.3f} seconds")
	last = end
	
'''
Zillow Data
'''
# Reads in the Zillow Data from the link that is from the Zillow Data Website and will always contain the most updated data
zillow = pd.read_csv('https://files.zillowstatic.com/research/public_csvs/zhvi/County_zhvi_uc_sfrcondo_tier_0.67_1.0_sm_sa_month.csv?t=1712270513')

# Reformatting dates and setting proper time range
zillow = reformat_dates(zillow)

# Adding county FIPS column using State FIPS and Municipal FIPS and dropping unnecessary columns
zillow = create_county_fips(zillow)

# Transforming each date column full of Zillow Values into separate instances with new Date and ZillowValue attributes
zillow = transpose_dates(zillow)

# Saving the cleaned Zillow data to a csv
zillow.to_csv("CleanedDataCSVs/zillow_cleaned.csv", sep=',', index=False, encoding='utf-8')

'''
Realtor Data
'''
# Reads in the Realtor Data from the link provided in the Realtor website that also hold up to date information
realtor = pd.read_csv('https://econdata.s3-us-west-2.amazonaws.com/Reports/Core/RDC_Inventory_Core_Metrics_Zip_History.csv', dtype = {"month_date_yyyymm": str, "county_fips": str})

# Dropping, renaming, and fixing columns in the realtor dataset
realtor = drop_and_rename(realtor)

# Saving the cleaned Realtor data to a csv
realtor.to_csv("CleanedDataCSVs/realtor_cleaned.csv", sep=',', index=False, encoding='utf-8')

'''
HUD USPS Data
'''
#Reading the ZIPS to County Crosswalk data from a previously downloaded file
zip_fip = pd.read_excel("DownloadedData/zip_to_county.xlsx", usecols = 'A:B')

# Renames the County column 
zip_fip.rename(columns={'COUNTY': 'county_fips'}, inplace=True)

# Saving the cleaned HUD USPS data to a csv
zip_fip.to_csv("CleanedDataCSVs/hudusps_cleaned.csv", sep=',', index=False, encoding='utf-8')

'''
State Abbreviation Data
'''
# Reading state abbreviations data from a previously downloaded file
# The link is likely not necessary because state abbreviations most likely will not change. Here is the link nonetheless.
# Link: https://www.google.com/url?sa=t&source=web&rct=j&opi=89978449&url=https://www.cdc.gov/wcms/4.0/cdc-wp/data-presentation/data/data-map-state-abbreviations.csv&ved=2ahUKEwjYtbOJvvGJAxWPkIkEHRWiI0UQFnoECBsQAQ&usg=AOvVaw26b07jCO4QjBfTPRtp8MXm
state_abbr = pd.read_csv("DownloadedData\data-map-state-abbreviations.csv")

# Fixing the instance with District of Columbia
state_abbr.at[9, 'Abbreviation'] = 'DC'

# Saving the cleaned State Abbreviation data to a csv
state_abbr.to_csv("CleanedDataCSVs/states_cleaned.csv", sep=',', index=False, encoding='utf-8')

'''
US Census: Comparative Housing Data
'''
# The download paths for each year of CP04 data. These should be downloaded previously and placed in the proper folder
cp0423_path = 'DownloadedData\ACSCP1Y2023.CP04-Data.csv'
cp0422_path = 'DownloadedData\ACSCP1Y2022.CP04-Data.csv'
cp0421_path = 'DownloadedData\ACSCP1Y2021.CP04-Data.csv'

# Reading the CSVs for each year and cleaning up the columns
cp0423 = read_set_year_cp04(cp0423_path, 2023)
cp0422 = read_set_year_cp04(cp0422_path, 2022)
cp0421 = read_set_year_cp04(cp0421_path, 2021)

# Adding columns with new attributes derived from the given data for each year
cp0423 = add_columns_cp04(cp0423)
cp0422 = add_columns_cp04(cp0422)
cp0421 = add_columns_cp04(cp0421)

# Combining the data frames from each year and sorting based on county and state
cp04 = pd.concat([cp0423, cp0422, cp0421], ignore_index = True)
cp04 = cp04.sort_values(by = ['county', 'State'])
cp04 = cp04.reset_index(drop = True)

# Saving the cleaned CP04 data to a csv
cp04.to_csv("CleanedDataCSVs/cp04_cleaned.csv", sep=',', index=False, encoding='utf-8')

'''
US Census: School Enrollment Data
'''
#Setting the path for the needed CSVs
school22_path = 'DownloadedData/ACSST5Y2022.S1401-Data.csv'
school21_path = 'DownloadedData/ACSST5Y2021.S1401-Data.csv'
school20_path = 'DownloadedData/ACSST5Y2020.S1401-Data.csv'

#Reads in the CSVs and adds a year column to their values
school22 = read_set_year_school(school22_path, 2022)
school21 = read_set_year_school(school21_path, 2021)
school20 = read_set_year_school(school20_path, 2020)

#Reformats the necessary columns and values to work with future functions
school22 = clean_columns_school(school22)
school21 = clean_columns_school(school21)
school20 = clean_columns_school(school20)

#Combines the data for al three years into a single dataset
cleaned_school = pd.concat([school22, school21, school20], ignore_index=True)
cleaned_school = cleaned_school.sort_values(by=['ZIP'])
cleaned_school = cleaned_school.reset_index(drop=True)

cleaned_school.to_csv("CleanedDataCSVs/school_cleaned.csv", sep=',', index=False, encoding='utf-8')

'''
US Census: Income Data
'''
#Setting the path for the needed CSVs
income22_path = 'DownloadedData/ACSST5Y2022.S1901-Data.csv'
income21_path = 'DownloadedData/ACSST5Y2021.S1901-Data.csv'
income20_path = 'DownloadedData/ACSST5Y2020.S1901-Data.csv'

#Reads in the CSVs and adds a year column to their values
income22 = read_set_year_income(income22_path, 2022)
income21 = read_set_year_income(income21_path, 2021)
income20 = read_set_year_income(income20_path, 2020)

#Combines the data for al three years into a single dataset
read_set_year_income = pd.concat([income22, income21, income20], ignore_index=True)
read_set_year_income = read_set_year_income.sort_values(by=['ZIP'])
read_set_year_income = read_set_year_income.reset_index(drop=True)

# Saving the cleaned income data to a csv
read_set_year_income.to_csv("CleanedDataCSVs/income_cleaned.csv", sep=',', index=False, encoding='utf-8')

'''
US Census: Population Data
'''
# This whole function from the clean_population.py file reads in the CSVs from DownloadedData,
# cleans the data, and outputs population_cleaned.csv and populationGrowth_cleaned.csv to CleanedDataCSVs
process_population_data()

'''
US Census: Diversity Data
'''
# This whole function from the clean_diversity.py file reads in the CSVs from DownloadedData,
# cleans the data, and outputs diversity_cleaned.csv and diversityGrowth_cleaned.csv to CleanedDataCSVs
process_diversity_data()

'''
Google Maps Data
'''
