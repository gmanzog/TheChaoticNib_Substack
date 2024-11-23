"""
https://data.cityofnewyork.us/Public-Safety/NYC-crime/qb7u-rbmr/about_data
"""
import pandas as pd


folder = 'C:/Users/gmger/OneDrive/Desktop/'
file = 'NYPD_Complaint_Data_Historic_20240923.csv'

df = pd.read_csv(folder + file, low_memory=False)

print("adding dates")
df['month'] = df['CMPLNT_FR_DT'].str.split("/").str[0]
df['day'] = df['CMPLNT_FR_DT'].str.split("/").str[1]
df['year'] = df['CMPLNT_FR_DT'].str.split("/").str[2]
df['my'] = df['month'] + "/" + df['year']
df.to_parquet(folder + "/NYPD_Complaint_Data_Historic_20240922.parquet")
import sys
sys.exit()