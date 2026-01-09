# LutronHousingDA
Team Repository for our Housing Data Analytics

## Team Members

### Students

Carlos Garro - cag224@lehigh.edu    
Joe Saponaro - jms225@lehigh.edu  
Louis Marca - lom225@lehigh.edu  
Zachary Porter - ztp226@lehigh.edu  

### Advisor

Alan Jeffery - arj323@lehigh.edu  

### Lutron

David Dolan - ddolan@lutron.com     
Namit Agrawal - ntagrawal@lutron.com    
Chunshan Liu - cliu@lutron.com

## Links

Google Drive link: https://drive.google.com/drive/folders/1vVzJc1xDx2jq7do3DMfhRNNueOEZNsA9?usp=sharing

Slack Link: https://capstoneproje-npk1596.slack.com

Jira Link: https://lehigh-lutron-capstone.atlassian.net/jira/software/projects/LHCP/boards/1?atlOrigin=eyJpIjoiNTRmZTk0ODhlYWIyNDJmNDhkOGM1NWU0YjllYzE4MzYiLCJwIjoiaiJ9

Confluence Link: https://lehigh-lutron-capstone.atlassian.net/wiki/x/CoAI

GitHub Link: https://github.com/CarlosG24/LutronHousingDA

## Content

### download_third_party_data.py

This script downloads all of the necessary third party data and cleans them in preparation to merge all data together.

- Downloads and cleans Zillow data
- Downloads and cleans Realtor data
- Cleans already-downloaded state abbreviations file
- Cleans already-downloaded HUD-USPS ZIP crosswalk file
- Cleans already-downloaded US Census data
	- Comparative Housing Characteristics (CP04)
	- School Enrollment (S1401)
	- Income in the Past 12 Months (S1901)
	- ACS Demographic and Housing Estimates (DP05)
		- Population and Diversity Data

#### helper_scripts_for_data_cleaning (folder)

This is the folder holding all the helper scripts to clean the data in this script.

- clean_cp04.py
- clean_diversity.py
- clean_income.py
- clean_population.py
- clean_realtor.py
- clean_school.py
- clean_zillow.py

#### Output CSVs

All the output CSVs are located in the CleanedDataCSVs folder.

- cp04_cleaned.csv
- diversity_cleaned.csv
- hudusps_cleaned.csv
- income_cleaned.csv
- population_cleaned.csv
- realtor_cleaned.csv
- school_cleaned.csv
- states_cleaned.csv
- zillow_cleaned.csv

### merge_datasets.py

This script merges all the cleaned data generated from download_third_party_data.py.

#### helper_scripts_for_data_merge (folder)

This is the folder holding all the helper scripts to merge the data in this script.

- merge_census_data.py
	- Holds a helper function to merge the CP04 data into the final dataset
	- Utilizes the state abbreviations data (states_cleaned.csv)
- merge_zillow_realtor.py
	- Merges the Zillow and Realtor datasets only
	- Utilizes the HUD USPS Zip Code Crosswalk data (hudusps_cleaned.csv)

#### Output CSVs

All the output CSVs are located in the CleanedDataCSVs folder.

- FinalData.csv
	- A final CSV that merges all the data sources together as according to the data merge infrastructure seen in the final documentation
- zillow_realtor_merged.csv
	- A CSV that contains just the Zillow and Realtor datasets merged together
	- This is used in later scripts that are used to prepare the data for various purposes

### prepare_data_for_dashboarding.py

This script prepares the data to be displayed on the Power BI dashboard.

- Reads in the merged Zillow and Realtor data (zillow_realtor_merged.csv)
- Merges in the three most recent years of US Census data into the three most recent years in the Zillow and Realtor data (2024, 2023, 2022)
	- Essentially, the US Census data is lagging behind the rest because it is not tracked and recorded as quickly
	- EXAMPLE:
		- The CP04 table contains data up until 2023 and the downloaded years are 2023, 2022, and 2021
		- The 2023 CP04 data gets mapped to the 2024 Zillow-Realtor data, 2022 to 2023, and 2021 to 2022
- Cleans and merges in the Lutron star rating data for matching cities 
- Outputs a full dataset to be used on the dashboard and a dataset containing only the most recent month

#### helper_scripts_for_data_prep (folder)

This is the folder holding all the helper scripts to merge the data in this script.

- merge_census_data.py
	- Merges in each US Census dataset with the lagging method described above
- merge_lutron_data.py
	- Cleans and merges the Lutron data into the dataset
	- Utilizes LutronData.csv from the DownloadedData folder

#### Output CSVs

All the output CSVs are located in the CleanedDataCSVs folder.

- cleaned_dashboard_data.csv
	- The CSV containing data to be used in the dashboard with all months and years included
- cleaned_dashbord_month_data.csv
	- The CSV containing data to be used in the dashboard with only the most recent month included

### prepare_data_for_model.py

This script prepares the data to be displayed on the Power BI dashboard.

- Reads in the merged Zillow and Realtor data (zillow_realtor_merged.csv)
- Merges in the three most recent years of US Census data into the three most recent years in the Zillow and Realtor data (2024, 2023, 2022)
	- Essentially, the US Census data is lagging behind the rest because it is not tracked and recorded as quickly
	- EXAMPLE:
		- The CP04 table contains data up until 2023 and the downloaded years are 2023, 2022, and 2021
		- The 2023 CP04 data gets mapped to the 2024 Zillow-Realtor data, 2022 to 2023, and 2021 to 2022
- Cleans and merges in the Lutron star rating data for matching cities
	- Keeping only the rows of data with star rating from Lutron
	- Aggregating the ZIP codes mapped to each city
- Outputs a dataset to be used to train the model

#### helper_scripts_for_data_prep (folder)

This is the folder holding all the helper scripts to merge the data in this script.

- merge_census_data.py
	- Merges in each US Census dataset with the lagging method described above
- merge_lutron_data.py
	- Cleans and merges the Lutron data into the dataset
	- Aggregates the ZIP codes within each city on their various attributes
	- Utilizes LutronData.csv from the DownloadedData folder

#### Output CSVs

All the output CSVs are located in the CleanedDataCSVs folder.

- cleaned_model_data.csv
	- The CSV containing the data to be used in training the model

### lutron_rating_analysis.ipynb

This script creates the ordinal regression model for predicting a city's Lutron star rating and displays the model's results.

- Reads in the cleaned model data (cleaned_model_data.csv)
- Splits the data into a training set and a test set
- Trains both a logit and probit ordinal regression model off predictor attributes
	- Attributes can be changed manually by editing the code
- Calculates the accuracy of each model
- Prints the accuracy, full summary, and the classification report for each model
- Displays a plot of the confusion matrix for each model

#### helper_scripts_for_model (folder)

This is the folder holding all the helper scripts to create the ordinal regression model.

- ordinal_regression_model.py
	- Converts the star ratings into an ordered categorical variable
	- Randomly splits the data into training and test sets
		- Still able to be recreated each time
	- Trains both the logit and probit models

### requirements.txt

### Visualizations (folder)

This folder contains Power BI and Jupyter Notebooks visualizations

### DownloadedData (folder)

zip_to_county.xlsx
- Provides a mapping from ZIP codes to county FIPS.
- County FIPS is the combination of State FIPS and Municipal FIPS concatenated together.
- This file is used in our code to merge data sets that contain only county FIPS with sets that contain ZIP codes.

ACSCP1Y2023.CP04-Data.csv, ACSCP1Y2022.CP04-Data.csv, ACSCP1Y2021.CP04-Data.csv
- Raw U.S Census Data containing Comparative Housing Characteristics for the years 2023,2022, and 2021.

data-map-state-abbreviations.csv
- Simple CSV that contains full U.S state names and their corresponding two-letter abbreviation.

LutronData.csv
- Contains a number of randomly selected cities where Lutron currently conducts business.
- For each city there is a star rating based off its sales performance for the year.

ACSST5Y2022.S1401.csv, 
- Raw U.S Census Data containing School Enrollment statistics in ZIP codes for the years 2023,2022, and 2021.


