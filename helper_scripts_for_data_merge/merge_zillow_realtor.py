import pandas as pd

def remove_dupes(data):
	# Sort values in by Zillow Value in descending order
	data.sort_values(by=['ZillowValue'], ascending=False)

	# Remove any duplicate instances after the first
	data = data.drop_duplicates(subset=["ZIP", "Date"], keep='first')

	return data

def add_year(data):
	# Inserting a column for the year data in the second position
	data.insert(1,"year", None)

	# Getting the year from the Date column
	data['year'] = (data['Date'] - (data['Date'] % 100)) / 100

	return data