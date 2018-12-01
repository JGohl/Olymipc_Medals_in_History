#app.py
#dependencies
import os
import pandas as pd
import numpy as np
import sqlalchemy
import pymysql
pymysql.install_as_MySQLdb()
# from sqlalchemy.ext.automap import automap_base
# from sqlalchemy.orm import Session
# from sqlalchemy import create_engine

#import SQL connection dependencies and establish parameters for SQL connection to amazon server
import sqlalchemy
import mysql.connector
from sqlalchemy import create_engine

#change values to new credentials
database_username = 'user_name_here'
database_password = 'password_here'
database_ip       = 'whatever.0.0.1:3306'
database_name     = 'olympics'
database_connection = sqlalchemy.create_engine('mysql+mysqlconnector://{0}:{1}@{2}/{3}'.
                                              format(database_username, database_password,
                                                     database_ip, database_name))

#convert csv files to data frames
f_winter = "data/winter.csv"
f_summer = "data/summer.csv"
f_dictionary = "data/dictionary.csv"
df_winter = pd.read_csv(f_winter, encoding = 'utf-8')
df_summer = pd.read_csv(f_summer, encoding = 'utf-8')                                                     
df_dictionary = pd.read_csv(f_dictionary, encoding = 'utf-8')

#add "season" column to df_winter for winter season
df_winter['season'] = "winter"

#add "season" column to df_summer for summer season
df_summer['season'] = "summer"

#merge all winter and summer data frames into one data frame
winter_and_summer_df = pd.concat([df_summer, df_winter])

#change dictionary_df column name of 'Country' to 'Country_full_name', and rename 'Code' to 'Country'
df_dictionary=df_dictionary.rename(columns = {'Country':'Country_full_name', 'Code':'Country'})

#merge dictionary into combined summer and winter data frame
master_data = pd.merge(winter_and_summer_df, df_dictionary, on='Country')

# convert master_data to SQL table, and then upload table to database using SQL connection, non-indexed
master_data.to_sql(name = 'master_data', con = database_connection, index=False, if_exists='append')


from flask import Flask, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)


#################################################
# Database Setup
#################################################

# app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db/bellybutton.sqlite"
db = SQLAlchemy(app)

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(db.engine, reflect=True)

# Save references to each table
Samples_Metadata = Base.classes.sample_metadata
Samples = Base.classes.samples


@app.route("/")
def index():
    """Return the homepage."""
    return render_template("index.html")


@app.route("/names")
def names():
    """Return a list of sample names."""

    # Use Pandas to perform the sql query
    stmt = db.session.query(Samples).statement
    df = pd.read_sql_query(stmt, db.session.bind)

    # Return a list of the column names (sample names)
    return jsonify(list(df.columns)[2:])


@app.route("/metadata/<sample>")
def sample_metadata(sample):
    """Return the MetaData for a given sample."""
    sel = [
        Samples_Metadata.sample,
        Samples_Metadata.ETHNICITY,
        Samples_Metadata.GENDER,
        Samples_Metadata.AGE,
        Samples_Metadata.LOCATION,
        Samples_Metadata.BBTYPE,
        Samples_Metadata.WFREQ,
    ]

    results = db.session.query(*sel).filter(Samples_Metadata.sample == sample).all()

    # Create a dictionary entry for each row of metadata information
    sample_metadata = {}
    for result in results:
        sample_metadata["sample"] = result[0]
        sample_metadata["ETHNICITY"] = result[1]
        sample_metadata["GENDER"] = result[2]
        sample_metadata["AGE"] = result[3]
        sample_metadata["LOCATION"] = result[4]
        sample_metadata["BBTYPE"] = result[5]
        sample_metadata["WFREQ"] = result[6]

    print(sample_metadata)
    return jsonify(sample_metadata)


@app.route("/samples/<sample>")
def samples(sample):
    """Return `otu_ids`, `otu_labels`,and `sample_values`."""
    stmt = db.session.query(Samples).statement
    df = pd.read_sql_query(stmt, db.session.bind)

    # Filter the data based on the sample number and
    # only keep rows with values above 1
    sample_data = df.loc[df[sample] > 1, ["otu_id", "otu_label", sample]]
    # Format the data to send as json
    data = {
        "otu_ids": sample_data.otu_id.values.tolist(),
        "sample_values": sample_data[sample].values.tolist(),
        "otu_labels": sample_data.otu_label.tolist(),
    }
    return jsonify(data)


if __name__ == "__main__":
    app.run()
