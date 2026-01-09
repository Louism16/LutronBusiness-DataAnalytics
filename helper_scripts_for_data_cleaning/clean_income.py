import pandas as pd

def read_set_year_income(path,year):
    # Reading the csv from a previously downloaded file
    income = pd.read_csv(path, header=None).iloc[1:].reset_index(drop=True)
    
    # Dropping unnecessary columns and selecting relevant ones
    income = (income.drop(columns=[0])  # Remove first column
                .iloc[:, :26]          # Keep first 27 columns
                .drop(columns=[3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 19, 21, 23, 25]))  # Remove columns 4-18, 20, 22, 24, 26

    # Removing the "ZCTA5 " prefix from ZIP codes
    income.iloc[:, 0] = income.iloc[:, 0].str.replace("ZCTA5 ", "", regex=False)

    # Renaming columns
    income.columns = income.iloc[0]  # Set first row as headers
    income = income[1:].reset_index(drop=True)  # Remove first row after setting it as header
    income.columns.values[:7] = ['ZIP', 'households_total', '100k_to_150k', '150k_to_200k', '200k_or_more', 'median_income', 'mean_income']

    # Adding the year column
    income.insert(2, "year", None)
    income['year'] = year  

    return income