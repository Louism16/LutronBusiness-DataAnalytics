import pandas as pd

def split_data_by_year_monthly(fullMerged):
	# Finding the most recent monthly date in the fully merged dataset and the same month 1 and 2 years prior
	current_month = fullMerged['Date'].max()
	last_year_month = current_month - 100
	two_year_month = last_year_month - 100

	# Filtering out for the real estate data for each month specified before
	current = fullMerged.loc[fullMerged.Date == current_month]
	lastYear = fullMerged.loc[fullMerged.Date == last_year_month]
	twoYear = fullMerged.loc[fullMerged.Date == two_year_month]

	# Returning a list of the dataframes contained the monthly data for all three years
	years = [current, lastYear, twoYear]
	return years

def split_data_by_year(fullMerged):
	# Finding the most recent year in the fully merged dataset
	year = fullMerged['year'].max()

	# Filtering out for the real estate data for each year
	current = fullMerged.loc[fullMerged.year == year]
	prior1 = fullMerged.loc[fullMerged.Date == (year - 1)]
	prior2 = fullMerged.loc[fullMerged.Date == (year - 2)]
	prior3 = fullMerged.loc[fullMerged.Date == (year - 3)]
	prior4 = fullMerged.loc[fullMerged.Date == (year - 4)]

	# Returning a list of the dataframes containing data for each year
	years = [current, prior1, prior2, prior3, prior4]
	return years

def merge_in_cp04(years):
	# Reading in the cleaned CP04 data
	cp04 = pd.read_csv("CleanedDataCSVs/cp04_cleaned.csv")

	# Splitting the CP04 data by year
	cp04_2023 = cp04[cp04["year"] == 2023]
	cp04_2022 = cp04[cp04["year"] == 2022]
	cp04_2021 = cp04[cp04["year"] == 2021]

	# Removing the year from the data
	cp04_2023 = cp04_2023.drop(['year'], axis = 1)
	cp04_2022 = cp04_2022.drop(['year'], axis = 1)
	cp04_2021 = cp04_2021.drop(['year'], axis = 1)

	# Merging each year of CP04 data with the corresponding dataframe from the years list
	years[0] = pd.merge(years[0], cp04_2023, on = ['county', 'State'], how = 'left')
	years[1] = pd.merge(years[1], cp04_2022, on = ['county', 'State'], how = 'left')
	years[2] = pd.merge(years[2], cp04_2021, on = ['county', 'State'], how = 'left')

	return years

def merge_in_school(years):
	# Reading the cleaned school enrollment data
	school = pd.read_csv("CleanedDataCSVs/school_cleaned.csv")

	# Splitting the school enrollment data by year
	school_2022 = school[school["year"] == 2022]
	school_2021 = school[school["year"] == 2021]
	school_2020 = school[school["year"] == 2020]

	# Removing the year from the data
	school_2022 = school_2022.drop(['year'], axis = 1)
	school_2021 = school_2021.drop(['year'], axis = 1)
	school_2020 = school_2020.drop(['year'], axis = 1)

	# Merging each year of school enrollment data with the corresponding dataframe from the years list
	years[0] = pd.merge(years[0], school_2022, on = 'ZIP', how = 'left')
	years[1] = pd.merge(years[1], school_2021, on = 'ZIP', how = 'left')
	years[2] = pd.merge(years[2], school_2020, on = 'ZIP', how = 'left')

	return years

def merge_in_income(years):
	# Reading the cleaned income data
	income = pd.read_csv("CleanedDataCSVs/income_cleaned.csv")

	# Splitting the income data by year
	income_2022 = income[income["year"] == 2022]
	income_2021 = income[income["year"] == 2021]
	income_2020 = income[income["year"] == 2020]

	# Removing the year from the data
	income_2022 = income_2022.drop(['year'], axis = 1)
	income_2021 = income_2021.drop(['year'], axis = 1)
	income_2020 = income_2020.drop(['year'], axis = 1)

	# Merging each year of income data with the corresponding dataframe from the years list
	years[0] = pd.merge(years[0], income_2022, on = 'ZIP', how = 'left')
	years[1] = pd.merge(years[1], income_2021, on = 'ZIP', how = 'left')
	years[2] = pd.merge(years[2], income_2020, on = 'ZIP', how = 'left')

	return years

def merge_in_population(years):
	# Reading the cleaned population data
	population = pd.read_csv("CleanedDataCSVs/population_cleaned.csv")

	# Splitting the population data by year
	population_2022 = population[population["year"] == 2022]
	population_2021 = population[population["year"] == 2021]
	population_2020 = population[population["year"] == 2020]

	# Removing the year from the data
	population_2022 = population_2022.drop(['year'], axis = 1)
	population_2021 = population_2021.drop(['year'], axis = 1)
	population_2020 = population_2020.drop(['year'], axis = 1)

	# Merging each year of population data with the corresponding dataframe from the years list
	years[0] = pd.merge(years[0], population_2022, on = 'ZIP', how = 'left')
	years[1] = pd.merge(years[1], population_2021, on = 'ZIP', how = 'left')
	years[2] = pd.merge(years[2], population_2020, on = 'ZIP', how = 'left')

	return years

def merge_in_diversity(years):
	# Reading the cleaned diversity data
	diversity = pd.read_csv("CleanedDataCSVs/diversity_cleaned.csv")

	# Splitting the diversity data by year
	diversity_2022 = diversity[diversity["year"] == 2022]
	diversity_2021 = diversity[diversity["year"] == 2021]
	diversity_2020 = diversity[diversity["year"] == 2020]

	# Removing the year from the data
	diversity_2022 = diversity_2022.drop(['year'], axis = 1)
	diversity_2021 = diversity_2021.drop(['year'], axis = 1)
	diversity_2020 = diversity_2020.drop(['year'], axis = 1)

	# Merging each year of diversity data with the corresponding dataframe from the years list
	years[0] = pd.merge(years[0], diversity_2022, on = 'ZIP', how = 'left')
	years[1] = pd.merge(years[1], diversity_2021, on = 'ZIP', how = 'left')
	years[2] = pd.merge(years[2], diversity_2020, on = 'ZIP', how = 'left')

	return years

def merge_in_growth(data):

	return data