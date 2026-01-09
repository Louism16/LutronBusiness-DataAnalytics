import pandas as pd

def weighted_average(dataframe, value, weight):
	# Computes the weighted average given a dataframe and value and weight columns
	val = pd.to_numeric(dataframe[value], errors='coerce')
	wt = pd.to_numeric(dataframe[weight], errors='coerce')
	return (val * wt).sum() / wt.sum()

def weighted_median(dataframe, value, weight):
	# Computes the weighted median given a dataframe and value and weight columns
	val = dataframe[value].reset_index(drop=True)
	wt = dataframe[weight].reset_index(drop=True)
	val = pd.to_numeric(val, errors='coerce')
	wt = pd.to_numeric(wt, errors='coerce')
	check = wt.sum() / 2
	# Store pairs of val and wt
	pairs = []
	for index in range(len(val)):
		if not pd.isna(val.iloc[index]) and not pd.isna(wt.iloc[index]):
			pairs.append([val.iloc[index], wt.iloc[index]])
	# Sort the list of pairs according to their values
	pairs.sort(key = lambda p: p[0])
	# If N is odd
	if len(val) % 2 != 0:
		# Traverse the set pairs from left to right
		sums = 0
		for element, weight in pairs:
			# Update sums
			sums += weight
			# If sum becomes > check
			if sums > check:
				return element
	# If N is even
	else:
		# For lower median traverse the set pairs from left
		sums = 0
		lowerMed = 0
		upperMed = 0
		for element, weight in pairs:
			# Update sums
			sums += weight
			# When sum >= check
			if sums >= check:
				lowerMed = element
				break
		# For upper median traverse the set pairs from right
		sums = 0
		for index in range(len(pairs)-1, -1, -1):
			element = pairs[index][0]
			weight = pairs[index][1]
			# Update sums
			sums += weight
			# When sum >= check
			if sums >= check:
				upperMed = element
				break
		return (float(lowerMed) + float(upperMed)) / 2

def clean_lutron_data(lutron):
	# Filtering out 2021 from the data which doesn't have any star ratings
	lutron = lutron[lutron["year"] >= 2022]

	# Reading in state abbreviation data to convert state names to abbreviations
	states = pd.read_csv("CleanedDataCSVs/states_cleaned.csv")

	# Creates a dictionary that maps state names to their abbreviations
	state_abbr = dict(zip(states["Name"], states["Abbreviation"]))

	# Creates the zip_name column with the city and state abbreviation
	lutron.insert(0,"zip_name", None)
	lutron["zip_name"] = (lutron["city"] + ", " + lutron["state"].map(state_abbr)).str.lower()

	# Drops the unnecessary columns in the data frame
	lutron.drop(["city", "state"], axis = 1, inplace = True)

	return lutron

def split_and_merge(lutron, years, for_model):
	# Split the lutron data into each of the three years
	lutron24 = lutron[lutron["year"] == 2024]
	lutron23 = lutron[lutron["year"] == 2023]
	lutron22 = lutron[lutron["year"] == 2022]

	# Setting the merge type depending on what the data is for
	#	If the data is for the model, the merge only includes instances with lutron data
	#	If the data is for the dashboard, the merge incldues all instances
	how = {for_model: 'left'}.get(True, 'right')

	# Merging the lutron data for each year with the rest of the data
	years[0] = pd.merge(lutron24, years[0], on = 'zip_name', how = how)
	years[1] = pd.merge(lutron23, years[1], on = 'zip_name', how = how)
	years[2] = pd.merge(lutron22, years[2], on = 'zip_name', how = how)

	# Filtering out missing ZIPs
	years[0] = years[0][years[0]['ZIP'].notna()]
	years[1] = years[1][years[1]['ZIP'].notna()]
	years[2] = years[2][years[2]['ZIP'].notna()]

	return years

def aggregate_zips(matchedData):
	# Dictionary to sum certain values when aggregating the zip codes
	agg_match = {'active_listing_count':'sum','total_listing_count':'sum','Enrollment':'sum','K-12':'sum','Undergrad':'sum','Grad':'sum','population':'sum','households_total':'sum'}

	# Aggregating all the columns that need to be summed using the agg_mathc dictionary
	aggregates = matchedData.groupby('zip_name').agg(agg_match)

	# Aggregating all other columns by applying a weighted average or a weighted median
	avgListPrice = (matchedData.groupby('zip_name').apply(weighted_average, 'average_listing_price', 'total_listing_count')).reset_index(name='average_listing_price')
	medListPrice = (matchedData.groupby('zip_name').apply(weighted_median, 'median_listing_price', 'total_listing_count')).reset_index(name='median_listing_price')
	medListPriceSqFt = (matchedData.groupby('zip_name').apply(weighted_median, 'median_listing_price_per_square_foot', 'total_listing_count')).reset_index(name='median_listing_price_per_square_foot')
	divIndex = (matchedData.groupby('zip_name').apply(weighted_average, 'simpson_diversity_index', 'population')).reset_index(name='simpson_diversity_index')
	hhRange1 = (matchedData.groupby('zip_name').apply(weighted_average, '100k_to_150k', 'households_total')).reset_index(name='100k_to_150k')
	hhRange2 = (matchedData.groupby('zip_name').apply(weighted_average, '150k_to_200k', 'households_total')).reset_index(name='150k_to_200k')
	hhRange3 = (matchedData.groupby('zip_name').apply(weighted_average, '200k_or_more', 'households_total')).reset_index(name='200k_or_more')
	avgInc = (matchedData.groupby('zip_name').apply(weighted_average, 'mean_income', 'households_total')).reset_index(name='mean_income')
	medInc = (matchedData.groupby('zip_name').apply(weighted_median, 'median_income', 'households_total')).reset_index(name='median_income')

	# Dropping columns set to be replaced by the new aggregated data
	matchedData.drop(['active_listing_count', 'total_listing_count', 'average_listing_price', 'median_listing_price', 'median_listing_price_per_square_foot', 'Enrollment', 'K-12', 'Undergrad', 'Grad', 'households_total', 'simpson_diversity_index', 'population', '100k_to_150k', '150k_to_200k', '200k_or_more', 'mean_income', 'median_income'], axis=1, inplace=True)

	# Dropping duplicate zip code instances because they are no longer needed once we merge with the aggregated data
	matchedData = matchedData.drop_duplicates(subset="zip_name", keep='first')

	# Merging in all the aggregated data so duplicate zip codes are now combined into one instance
	matchedData = pd.merge(matchedData, aggregates, on = 'zip_name', how = 'left')
	matchedData = pd.merge(matchedData, avgListPrice, on = 'zip_name', how = 'left')
	matchedData = pd.merge(matchedData, medListPrice, on = 'zip_name', how = 'left')
	matchedData = pd.merge(matchedData, medListPriceSqFt, on = 'zip_name', how = 'left')
	matchedData = pd.merge(matchedData, divIndex, on = 'zip_name', how = 'left')
	matchedData = pd.merge(matchedData, hhRange1, on = 'zip_name', how = 'left')
	matchedData = pd.merge(matchedData, hhRange2, on = 'zip_name', how = 'left')
	matchedData = pd.merge(matchedData, hhRange3, on = 'zip_name', how = 'left')
	matchedData = pd.merge(matchedData, avgInc, on = 'zip_name', how = 'left')
	matchedData = pd.merge(matchedData, medInc, on = 'zip_name', how = 'left')

	return matchedData