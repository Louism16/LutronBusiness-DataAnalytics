import pandas as pd

def merge_cp04_states(cp04):
	state_abbr = pd.read_csv("CleanedDataCSVs/states_cleaned.csv")
	cp04 = pd.merge(cp04, state_abbr, left_on = 'State', right_on = 'Name')
	cp04.drop(['State','Name'], axis = 1, inplace = True)
	cp04.rename(columns={'Abbreviation':'State'}, inplace = True)

	return cp04