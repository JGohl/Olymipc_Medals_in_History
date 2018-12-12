# 0 Full Data Stack Project Outline
# phases of the data: going from raw data to end-user
# Big Picture:
# ( Server Side )  --Data+Code-->  ( Client Side )
# Broken Down:
# ( CSV Files --> Pandas DataFrame --> MySQL DB  --Data-->  Flask Server )  --Data+Code-->  ( JS --html--> DOM )
# steps:
# 1 obtain and convert raw CSV datasets into DataFrames using Pandas
# 2 clean DataFrames
# 3 combine the cleaned DataFrames into single master DataFrame
# 4 upload master DataFrame to MySQL DB running on AWS cloud server
# 5 create and run flask http server running also on AWS cloud server
# 6 using flask, send basic request to MySQL DB, get response back as json data
# 7 examine json data
# 8 add javascript visualization libraries to flask server
# 9 configure javascript visualization libraries to parse the json data
# 10 client receives data and html
# 11 client then renders data as visualization on client side DOM in HTML

print('Full Data Stack now starting up..')
print('This process will perform the following actions:')
print('( CSV Files --> Pandas DataFrame --> MySQL DB  --Data-->  Flask Server )  --Data+Code-->  ( JS --html--> DOM )')
print('----------------------------------')

# 1 
# obtain and convert raw CSV datasets into DataFrames using Pandas
print('Initializing..')
print('----------------------------------')

# dependencies
import pandas as pd
import os
import numpy as np

#ensure entire link is displayed in dataframes
pd.set_option('display.max_colwidth', -1)

print('Now reading CSV files...')
# set file paths for reading csv files
f_winter = "data/winter.csv"
f_summer = "data/summer.csv"
f_dictionary = "data/dictionary.csv"
f_coord = "data/country-capitals.csv"
f_maps = "data/country_flags.csv"
print('Reading of CSV files completed.')
print('----------------------------------')

# convert csv files into dataframes
print('Now converting CSV files into DataFrames...')
df_winter = pd.read_csv(f_winter, encoding = 'utf-8')
df_summer = pd.read_csv(f_summer, encoding = 'utf-8')                                                     
df_dictionary = pd.read_csv(f_dictionary, encoding = 'utf-8')
df_coord = pd.read_csv(f_coord, encoding = 'utf-8')
df_maps = pd.read_csv(f_maps, encoding = 'utf-8')

print('Conversion of CSV files into DataFrames completed.')
print('----------------------------------')

# 2
# clean DataFrames
print('Now cleaning DataFrames...')
# add "season" column to df_winter for winter season
df_winter['season'] = "winter"

# add "season" column to df_summer for summer season
df_summer['season'] = "summer"

# identify columns and shape for summer data
print('Columns and shape for summer data:')
print(df_summer.columns)
print(df_summer.shape)
print('----------------------------------')

# identify columns and shape for winter data
print('Columns and shape for winter data:')
print(df_winter.columns)
print(df_winter.shape)
print('----------------------------------')

# identify columns and shape for dictionary data
print('Columns and shape for dictionary data:')
print(df_dictionary.columns)
print(df_dictionary.shape)
print('----------------------------------')

# search for any nan values in summer data
nan_summer = df_summer[df_summer.isnull().any(axis=1)]
print("Any nan values in summer data, to be fixed downstream:")
print(nan_summer)
print('----------------------------------')

# search for any nan values in winter data
nan_winter = df_winter[df_winter.isnull().any(axis=1)]
print("Any nan values in winter data, to be fixed downstream:")
print(nan_winter)
print('...')
print('No nan values in winter data found')
print('----------------------------------')

# update Nan values in summer data:
# update row 29603, athlete is Alptekin, Cakir,  country is TUR 
print('Now updating nan values in summer data...')
df_summer.at[29603, 'Athlete'] = "Alptekin, Cakir"
df_summer.at[29603, 'Country'] = "TUR"

# update row 31072, athlete is Maneza, Maiya, country is KAZ
df_summer.at[31072, 'Athlete'] = "Maneza, Maiya"
df_summer.at[31072, 'Country'] = "KAZ"

# update row 31091, athlete is Ilyin, Ilya, country is KAZ
df_summer.at[31091, 'Athlete'] = "Ilyin, Ilya"
df_summer.at[31091, 'Country'] = "KAZ"

# update row 31110, country is RUS
df_summer.at[31110, 'Country'] = "RUS"
print('Update of nan values in summer data completed')
print('----------------------------------')

# identify all unique values of country codes for summer data
summer_country_codes = df_summer['Country'].unique()
print("Unique values of country codes for summer data:")
print(summer_country_codes)
print('----------------------------------')

# identify all unique values of country codes for winter data
winter_country_codes = df_winter['Country'].unique()
print("Unique values of country codes for winter data:")
print(winter_country_codes)
print('----------------------------------')

# check if summer_country_codes contains a country code value not in the dictionary
bad_summer_codes = [item for item in summer_country_codes if item not in df_dictionary['Code'].unique()]
print('Any country codes in the summer data not present in the dictionary data:')
print(bad_summer_codes)
print('----------------------------------')

# check if winter_country_codes contains a country code value not in the dictionary
bad_winter_codes = [item for item in winter_country_codes if item not in df_dictionary['Code'].unique()]
print('Any country codes in the winter data not present in the dictionary data:')
print(bad_winter_codes)
print('----------------------------------')

# manually look up bad country codes on google and replace them with valid ones in the dictionary
print('''
All of the bad country codes to be changed in summer and winter data:
ANZ = new zealand, NZL
BOH = bohmeia, now CZE
BWI = british west indies, now JAM
EUA = east germany, now GER
EUN = ussr unified team, now RUS
FRG = west germany, now GER
GDR = east germany saxony, now GER
IOP = yugoslavia, now SCG
MNE = now soverign state of montegro, was SCG
ROU = romania, now ROM
RU1 = russian empire, now RUS
SGP = singapore, now SIN
SRB = serbia, now SCG
TCH = czechoslovakia, now CZE
TTO = Trinidad and Tobago, now TRI
URS = ussr, now RUS
YUG = yugoslavia, now SCG
ZZX = mixed team, now VARIOUS
''')
print("Now updating country code changes...")
df_summer = df_summer.replace("ANZ", "NZL")
df_summer = df_summer.replace("BOH", "CZE")
df_summer = df_summer.replace("BWI", "JAM")
df_summer = df_summer.replace("EUA", "GER")
df_summer = df_summer.replace("EUN", "RUS")
df_summer = df_summer.replace("FRG", "GER")
df_summer = df_summer.replace("GDR", "GER")
df_summer = df_summer.replace("IOP", "SCG")
df_summer = df_summer.replace("MNE", "SCG")
df_summer = df_summer.replace("ROU", "ROM")
df_summer = df_summer.replace("RU1", "RUS")
df_summer = df_summer.replace("SGP", "SIN")
df_summer = df_summer.replace("SRB", "SCG")
df_summer = df_summer.replace("TCH", "CZE")
df_summer = df_summer.replace("TTO", "TRI")
df_summer = df_summer.replace("URS", "RUS")
df_summer = df_summer.replace("YUG", "SCG")
df_summer = df_summer.replace("ZZX", "VARIOUS")
df_winter = df_winter.replace("ANZ", "NZL")
df_winter = df_winter.replace("BOH", "CZE")
df_winter = df_winter.replace("BWI", "JAM")
df_winter = df_winter.replace("EUA", "GER")
df_winter = df_winter.replace("EUN", "RUS")
df_winter = df_winter.replace("FRG", "GER")
df_winter = df_winter.replace("GDR", "GER")
df_winter = df_winter.replace("IOP", "SCG")
df_winter = df_winter.replace("MNE", "SCG")
df_winter = df_winter.replace("ROU", "ROM")
df_winter = df_winter.replace("RU1", "RUS")
df_winter = df_winter.replace("SGP", "SIN")
df_winter = df_winter.replace("SRB", "SCG")
df_winter = df_winter.replace("TCH", "CZE")
df_winter = df_winter.replace("TTO", "TRI")
df_winter = df_winter.replace("URS", "RUS")
df_winter = df_winter.replace("YUG", "SCG")
df_winter = df_winter.replace("ZZX", "VARIOUS")
print('Country code update complete for summer and winter data.')
print('----------------------------------')
# to make things easier to understand, the country column for both winter and summer dataframes will now be renamed to "Country_Code"
print('Now renaming country column in both summer and winter dataframes to Country_code.')
df_summer = df_summer.rename(columns = {'Country':'Country_code'})
df_winter = df_winter.rename(columns = {'Country':'Country_code'})
print('Renaming of country columns in summer and winter dataframes to Country_code completed.')
print('----------------------------------')
print('Now renaming columns in dictionary dataframe, Country to Country_name, and Code to Country_code.')
df_dictionary = df_dictionary.rename(columns = {'Code':'Country_code'})
df_dictionary['Country'] = [x.strip('*') for x in df_dictionary.Country]
print('Renaming of columns in dictionary completed.')
print('----------------------------------')
print('Now renaming columns in coord dataframe, Country to CountryName to Country. Dropping Countr_code column. Stripping asterisk from Country column')
df_coord = df_coord.rename(columns = {'CountryName':'Country'})
df_coord = df_coord.drop(columns = ['CountryCode'])
print('Renaming and cleaning of columns in dictionary completed.')
print('----------------------------------')

# 3 
# combine the cleaned DataFrames into single master DataFrame

# concat winter and summer data frames into one dataframe
print('Now combining dataframes into single master dataframe...')
winter_and_summer_df = pd.concat([df_summer, df_winter])

# merge dictionary, coord, and map dataframes
df_dict_coord = pd.merge(df_dictionary, df_coord, how="left", on="Country")
df_dict_coord_maps = pd.merge(df_dict_coord, df_maps, how="left", on="Country")

# merge dictionary/coord/map dataframe into combined summer and winter data frame
master_data = pd.merge(winter_and_summer_df, df_dict_coord_maps, how='left', on='Country_code')

# drop all rows where the country is ZZX or Various mixed teams
master_data.drop(master_data.loc[master_data['Country_code']=='VARIOUS'].index, inplace=True)

# add coordinates for South Korea
#master_data.loc[master_data['Country_code'] == 'KOR', ['CapitalLatitude', 'CapitalLongitude', 'CapitalName']] = ['37.5665', '126.9780', 'Seoul']

# add an id index to master dataframe
master_data['id'] = range(1, len(master_data) + 1)

# # search for any nan GDP values in master data
# nan_master_data = master_data[master_data['GDP per Capita'].isnull()]

# print("Any nan values in master_data, to be fixed downstream:")
# print(nan_master_data)
# print('----------------------------------')
# print(len(nan_master_data))

# # fill NaN GDP per Capita values with 0
# master_data['GDP per Capita'] = master_data.fillna(0)

# print('Creation of single master dataframe complete.')
# print('----------------------------------')
# print('Now previewing and getting shape of master_data...')
# print(master_data.shape)
# print(master_data.head(3))
# print('----------------------------------')

# # search for any nan Population values in master data
# nan_master_data = master_data[master_data['Population'].isnull()]

# print("Any nan values in master_data, to be fixed downstream:")
# print(nan_master_data)
# print('----------------------------------')
# print(len(nan_master_data))

# # fill NaN Population values with 0
# master_data['Population'] = master_data.fillna(0)

# print('Creation of single master dataframe complete.')
# print('----------------------------------')
# print('Now previewing and getting shape of master_data...')
# print(master_data.shape)
# print(master_data.head(3))
# print('----------------------------------')

# 4 
# upload master DataFrame to MySQL DB running on AWS cloud server

print('Now Converting and uploading master DataFrame to MySQL DB...')

import sqlalchemy
import pymysql
pymysql.install_as_MySQLdb()

#change values to new credentials
database_username = 'root'
database_password = 'password'
database_ip       = '127.0.0.1:3306'
database_name     = 'olympics'
database_connection = sqlalchemy.create_engine('mysql+mysqlconnector://{0}:{1}@{2}/{3}'.
                                              format(database_username, database_password,
                                                     database_ip, database_name))
                                                     
# convert master_data to SQL table, and then upload table to database using SQL connection, non-indexed
master_data.to_sql(name = 'master_data', con = database_connection, index=False, if_exists='replace', chunksize = 1000)
with database_connection.connect() as con:
    con.execute('ALTER TABLE `olympics`.`master_data` ADD PRIMARY KEY (`id`);')

print('DataFrame upload to MySQL DB completed.')
print('----------------------------------')

# 5 create and run flask http server running also on AWS cloud server
# dependencies

from flask import Flask, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
print('Now Connecting to MySQL server for query results..')
mysql_query_df = pd.read_sql("SELECT * FROM olympics.master_data", con = database_connection)
print('Now Jsonifying MySql Query..')
json_data = mysql_query_df.to_json(orient='records')
print('Now starting flask server')
app = Flask(__name__)
@app.route("/")
def index():
    '''Return to the homepage.'''
    return render_template('index.html')
    
@app.route("/map")
def map():
    '''Return to the map visual.'''
    return render_template('map.html')

@app.route("/data")
def data():
    """Return the json data"""
    return json_data
if __name__ == "__main__":
    app.run()