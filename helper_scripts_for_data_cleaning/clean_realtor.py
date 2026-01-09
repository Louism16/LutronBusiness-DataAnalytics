import pandas as pd

def drop_and_rename(realtor):
	# Removes all uneeded columns from the dataset
	realtor.drop(['price_increased_count_mm', 'price_increased_count_yy', 'quality_flag','median_listing_price_mm', 'median_listing_price_yy', 'active_listing_count_mm', 'active_listing_count_yy', 'median_days_on_market', 'median_days_on_market_mm', 'median_days_on_market_yy', 'new_listing_count', 'new_listing_count_mm', 'new_listing_count_yy', 'price_increased_count', 'price_reduced_count', 'price_reduced_count_mm', 'price_reduced_count_yy', 'pending_listing_count', 'pending_listing_count_mm', 'pending_listing_count_yy', 'median_listing_price_per_square_foot_mm', 'median_listing_price_per_square_foot_yy', 'median_square_feet', 'median_square_feet_mm', 'median_square_feet_yy', 'average_listing_price_mm', 'average_listing_price_yy', 'total_listing_count_mm', 'total_listing_count_yy', 'pending_ratio', 'pending_ratio_mm', 'pending_ratio_yy'], axis=1, inplace=True)

	# Removes the final row which doesnt contain area data
	realtor = realtor.iloc[:-1]

	# Renames the date column and keeps only the date range that we are looking for
	realtor.rename(columns={'month_date_yyyymm':'Date'}, inplace=True)
	realtor['Date'] = realtor['Date'].astype(int)
	realtor = realtor[realtor["Date"] >= 202001]  # remove all rows that have months before Jan 2020
	realtor = realtor[realtor["Date"] <= 202408]  # remove all rows that have months after Aug 2024

	# Renames the postal code column
	realtor.rename(columns={'postal_code':'ZIP'}, inplace = True)

	return realtor