import pandas as pd

#Reads in the school year CSV, keeps only the necessary columns, renames the columns, and adds a year column that is set to the given year
def read_set_year_school(path, year):
    schoolData = pd.read_csv(path)
    schoolData = schoolData[["NAME","S1401_C01_001E","S1401_C01_003E", "S1401_C01_008E","S1401_C01_009E"]]
    schoolData.rename(columns={'S1401_C01_001E': 'Enrollment', 'NAME': 'ZIP', 'S1401_C01_003E' : 'K-12', 'S1401_C01_008E' : 'Undergrad', 'S1401_C01_009E' : 'Grad'}, inplace=True)
    schoolData.drop(0, inplace=True)
    schoolData = schoolData.reset_index(drop=True)
    schoolData.insert(5,"year", None)
    schoolData['year'] = year
    
    return schoolData

#This reformats the ZIP column so that only the 5-digit ZIP code is kept, and turns any columns with number values from a string to an integer datatype
def clean_columns_school(data):
    ## Seperates the Zip Code Digits from the Zip Column
    for row in data.index :
        data.iloc[row,0] = int(data.iloc[row,0][5:11])

    ## Turns the numbered values into int types
    for ind in data.index:
        numString =  data.iloc[ind, 1]
        numString2 =  data.iloc[ind, 2]
        numString3 =  data.iloc[ind, 3]
        numString4 =  data.iloc[ind, 4]
    if type(numString) is str:
        numString = numString.replace(',', '')
        data.iloc[ind, 1] = int(numString)
    if type(numString2) is str:
        numString2 = numString2.replace(',', '')
        data.iloc[ind, 2] = int(numString2)
    if type(numString3) is str:
        numString3 = numString3.replace(',', '')
        data.iloc[ind, 3] = int(numString3)
    if type(numString4) is str:
        numString4 = numString4.replace(',', '')
        data.iloc[ind, 4] = int(numString4)
    
    return data
    