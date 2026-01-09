import pandas as pd

def reformat_dates(zillow):
	# Will reformat the date columms in the Zillow data to the same format as the date column in the realtor data
	for col_name in zillow.columns:     
		if col_name[0].isdigit():
			newDate = col_name[:7].replace('-',"")
			zillow.rename(columns={col_name:newDate}, inplace=True)

	# Removes all columns that are before Jan 2020 leaving only our desired time range
	zillow = zillow.drop(zillow.loc[:, '200001':'201912'].columns, axis=1)

	return zillow

def create_county_fips(zillow):
	# Create a new column in Zillow for county fips that will then be used to merge with the Realtor Data. 
	# Coutry Fip is made out of the StateCode FIPS(2 digits) and the Municpal Code Fips(3 digits) by just concatenating in that order
	zillow.insert(2,"county_fips", None)
	zillow['county_fips'] = (zillow['StateCodeFIPS'] * 1000) + zillow['MunicipalCodeFIPS']

	# Renaming and dropping certain columns
	zillow.rename(columns={'RegionName':'county'}, inplace = True)
	zillow.drop(['StateCodeFIPS', 'MunicipalCodeFIPS', 'SizeRank', 'RegionType', 'StateName'], axis = 1, inplace = True)

	return zillow

def transpose_dates(zillow):
	# Create a data frame with just the columns with identifying attributes and no dates
	zillowMerge = zillow.iloc[0:0, 0:5]

	# Adding columns for Date and Zillow Value
	zillowMerge["Date"] = None
	zillowMerge["ZillowValue"] = None

	# For each date column in the original data frame, create instances for each county with the Date and Zillow Value
	for col_name in zillow.columns:
		if col_name[0].isdigit():
			zillowMonth = zillow.iloc[:, 0:5]
			zillowMonth["Date"] = col_name
			zillowMonth["ZillowValue"] = zillow[col_name]
			zillowMerge = pd.concat([zillowMerge, zillowMonth])

	return zillowMerge