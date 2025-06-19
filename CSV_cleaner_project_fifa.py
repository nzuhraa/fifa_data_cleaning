import pandas as pd 
import numpy as np 

filename = r"C:\PYTHON STUDY\CSV_cleaner_fifa\fifa21_raw_data_v2.csv"
df = pd.read_csv(filename)

## Checking how sample data looks
print(df.head(5))

print("Number of columns: ", df.shape[1])
print("Number of rows: ", df.shape[0])

## Sorting values:
df.sort_values(by = "ID", inplace  = True)

## I want to see all the rows, so changing display option to max:
pd.set_option('display.max_rows', None)

print("Number of unique values in the Height column including NULL: ", df['Height'].nunique(dropna=False))
print(df.value_counts("Height", dropna=False))

## Function to convert height values to cm:
def any_to_cm(any_str):
    try:
        if pd.isna(any_str):
            return None
        if "cm" in any_str:
            return int(any_str.replace("cm",""))
        if "'" in any_str:
            parts = any_str.replace('"','').split("'")
            feet = int(parts[0])
            inches = int(parts[1])
            return int(round(feet*30.48 + inches*2.54,0))
    except (ValueError, IndexError):
        return None

## Applying newly created function to Height column:    
df["Height"] = df["Height"].apply(any_to_cm)

## Checking values after applying function, displaying sorted from shortest height to tallest:
#print(df.value_counts("Height", dropna=False).sort_index())

## Function to convert weight values to kg:
def any_to_kg(any_str):
    try:
        if pd.isna(any_str):
            return None
        if any_str.endswith("kg"):
            return int(any_str.replace("kg",""))
        if any_str.endswith("lbs"):
            return int(round(0.453592*float(any_str.replace("lbs","")),0))
    except (ValueError, IndexError):
        return None

## Applying newly created function to Weight column:
df["Weight"] = df["Weight"].apply(any_to_kg)

#print(df.value_counts("Weight", dropna= False).sort_index())

#print(df["Value"].value_counts(dropna=False))

## Function to convert any value to integer:
def any_to_money(any_str):
    try:
        if pd.isna(any_str):
            return None
        any_str = any_str.replace("€","").replace(".","")
        if any_str.isdigit():
            return int(any_str)
        if any_str.endswith("K"):
            return int(any_str.replace("K",""))*1000
        if any_str.endswith("M"):
            return int(any_str.replace("M",""))*1000000
    except (ValueError, IndexError):
        return None
    
## Applying newly created function to Value, Wage, Release Clause columns:
df["Value"] = df["Value"].apply(any_to_money)
df["Wage"] = df["Wage"].apply(any_to_money)
df["Release Clause"] = df["Release Clause"].apply(any_to_money)

print(df.dtypes)

## Writing clean data to new csv file:
df.to_csv(r"C:\PYTHON STUDY\CSV_cleaner_fifa\fifa21_clean_data_v2.csv", index=False)