from flask_sqlalchemy import SQLAlchemy
from flask import Flask, jsonify, render_template
import os

import pandas as pd
import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
import pymysql
pymysql.install_as_MySQLdb()

#change values to new credentials
database_username = 'root'
database_password = 'root'
database_ip = '127.0.0.1:3306'
database_name = 'olympics'
database_connection = sqlalchemy.create_engine('mysql+mysqlconnector://{0}:{1}@{2}/{3}'.
                                               format(database_username, database_password,
                                                      database_ip, database_name))

#Flask Initialize
print('Now starting flask server')
app = Flask(__name__)
#################################################
# Database Setup
#################################################

app.config["SQLALCHEMY_DATABASE_URI"] = 'mysql+mysqlconnector://{0}:{1}@{2}/{3}'.format(
    database_username, database_password, database_ip, database_name)
db = SQLAlchemy(app)

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(db.engine, reflect=True)

# Save references to each table
Master_data = Base.classes.master_data
####################################################
##Jsonify to convert data, pd.to_json for dataframes
####################################################

print('Now Connecting to MySQL server for query results..')
mysql_query_df = pd.read_sql(
    "SELECT * FROM olympics.master_data", con=database_connection)
print('Now Jsonifying MySql Query..')
json_data = mysql_query_df.to_json(orient='records')


@app.route("/")
def index():
    '''Return to the homepage.'''
    return render_template('index.html')

#@app.route("/data/<select1>/<select2>/")


@app.route("/data_no-variable/")
def data():
    #If you wish to return data that is independent of selection variables,
    #You can do the processing to calculate the data to return on server instead of client.
    """Return the json data"""
    return json_data

#
@app.route("/data2/")
def data2():
    stmt = db.session.query(Master_data).statement
    dataframe = pd.read_sql_query(stmt, db.session.bind)
    """Return the json data"""
    json_data2 = dataframe.to_json(orient='records')
    return json_data2

@app.route("/summer/<year>")
def summer_year(year):
    stmt = db.session.query(Master_data).\
    filter(Master_data.season == "summer").\
    filter(Master_data.Year == year).\
    statement
    dataframe = pd.read_sql_query(stmt, db.session.bind)
    #return the dataframe as json
    json_df = dataframe.to_json(orient='records')
    return json_df

    
if __name__ == "__main__":
    app.run()
