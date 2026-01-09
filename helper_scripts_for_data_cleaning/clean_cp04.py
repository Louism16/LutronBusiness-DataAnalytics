import pandas as pd

def read_set_year_cp04(path, year):
    # Reading the csv from a previously downloaded file
    cp04 = pd.read_csv(path)
    
    # Selecting the necessary columns and renaming them
    col = "CP04_" + str(year) + "_08"
    cols = [col + "0E", col + "7E", col + "8E", col + "9E"]
    cp04 = cp04[["NAME", cols[0], cols[1], cols[2], cols[3]]]
    cp04.rename(columns={cols[0]:'units', cols[1]:'500k_to_1m', cols[2]:'1m_or_more', cols[3]:'median'}, inplace=True)
    
	# Removing the first row which does not contain actual data and resetting the index
    cp04.drop(0, inplace=True)
    cp04 = cp04.reset_index(drop=True)
    
	# Splitting the name column into county and state
    cp04.insert(1, "county", None)
    cp04.insert(2, "State", None)
    cp04['county'] = cp04['NAME'].str.split(', ', expand = True)[0]
    cp04['State'] = cp04['NAME'].str.split(', ', expand = True)[1]
    cp04.drop('NAME', axis = 1, inplace = True)
    
	# Inserting the year column in the dataframe
    cp04.insert(2,"year", None)
    cp04['year'] = year
    
    return cp04

def add_columns_cp04(cp04):
	# Converting columns to numerics
	cp04['units'] = pd.to_numeric(cp04['units'], errors='coerce')
	cp04['500k_to_1m'] = pd.to_numeric(cp04['500k_to_1m'], errors='coerce')
	cp04['1m_or_more'] = pd.to_numeric(cp04['1m_or_more'], errors='coerce')
      
	# Creating new columns based on the given data
	cp04['500k_or_more'] = cp04['500k_to_1m'] + cp04['1m_or_more']
	cp04['density_rating'] = cp04['1m_or_more'] * 0.75 + cp04['500k_to_1m'] * 0.25
	cp04['num_500k_to_1m'] = cp04['units'] * cp04['500k_to_1m']
	cp04['num_1m_or_more'] = cp04['units'] * cp04['1m_or_more']
	cp04['num_500k_or_more'] = cp04['num_500k_to_1m'] + cp04['num_1m_or_more']
	cp04['volume_rating'] = cp04['num_1m_or_more'] * 0.75 + cp04['num_500k_to_1m'] * 0.25
    
	return cp04
    