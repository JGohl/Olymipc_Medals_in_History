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

@app.route("/")
def index():
    '''Return to the homepage.'''
    return render_template('index_winter.html')


#metadata
@app.route("/summer/<year>/<sport>")
def summer_records_ajz(year, sport):
    stmt = db.session.query(Master_data.Year, Master_data.City, Master_data.Sport, Master_data.Discipline, Master_data.Event, Master_data.Gender, Master_data.Country_code, Master_data.Country, Master_data.Medal).\
    filter(Master_data.season == "summer").\
    filter(Master_data.Year == year).\
    filter(Master_data.Sport == sport).\
    statement
    dataframe = pd.read_sql_query(stmt, db.session.bind)
    #return the dataframe as jsonict()
    json_data = dataframe.to_json(orient='records')
    return json_data
    
#metadata for visual
@app.route("/summer/<year>/<sport>/vis1")
def summer_dict_ajz(year, sport):
    stmt = db.session.query(Master_data.Year, Master_data.City, Master_data.Sport, Master_data.Discipline, Master_data.Event, Master_data.Gender, Master_data.Country_code, Master_data.Country, Master_data.Medal).\
    filter(Master_data.season == "summer").\
    filter(Master_data.Year == year).\
    filter(Master_data.Sport == sport).\
    statement
    dataframe = pd.read_sql_query(stmt, db.session.bind)
    #return the dataframe as json
    medal_df = pd.DataFrame(dataframe.groupby(['Country','Medal']).count()['Year'])
    medal_df.columns=['Count']
    medal_dict = medal_df.groupby(level=0).apply(lambda df: df.xs(df.name).to_dict()).to_dict()
    return jsonify(medal_dict)

#important
@app.route("/summer/<year>/<sport>/<medal>")
def summer_vis_ajz(year, sport, medal):
    stmt = db.session.query(Master_data.Year, Master_data.City, Master_data.Sport, Master_data.Discipline, Master_data.Event, Master_data.Gender, Master_data.Country_code, Master_data.Country, Master_data.Medal).\
    filter(Master_data.season == "summer").\
    filter(Master_data.Year == year).\
    filter(Master_data.Sport == sport).\
    statement
    dataframe = pd.read_sql_query(stmt, db.session.bind)
    #return the dataframe as json
    if medal != "Total":
        medal_df = dataframe.loc[dataframe.Medal == medal]
        medal_df = pd.DataFrame(medal_df.groupby('Country').count()['Medal']).sort_values('Medal',ascending=False).reset_index()
        json_data = medal_df.to_json(orient='records')
    else:
        medal_df = dataframe
        medal_df = pd.DataFrame(medal_df.groupby('Country').count()['Medal']).sort_values('Medal',ascending=False).reset_index()
        json_data = medal_df.to_json(orient='records')
    return json_data

#important
@app.route("/summer/filters")
def summer_filters_ajz():
    """Return lists for filter options"""
    #Year, Sport, Country
    stmt = db.session.query(Master_data.Year, Master_data.City, Master_data.Sport, Master_data.Discipline, Master_data.Event, Master_data.Gender, Master_data.Country_code, Master_data.Country, Master_data.Medal).\
    filter(Master_data.season =="summer").\
    statement
    dataframe = pd.read_sql_query(stmt, db.session.bind)
    years = dataframe.Year.unique().tolist()
    years.sort(reverse=True)
    data = {
        "years": years,
        "sports": dataframe.Sport.unique().tolist()
    }
    return jsonify(data)

@app.route("/winter/<year>/<sport>")
def winter_records_ajz(year, sport):
    stmt = db.session.query(Master_data.Year, Master_data.City, Master_data.Sport, Master_data.Discipline, Master_data.Event, Master_data.Gender, Master_data.Country_code, Master_data.Country, Master_data.Medal).\
    filter(Master_data.season == "winter").\
    filter(Master_data.Year == year).\
    filter(Master_data.Sport == sport).\
    statement
    dataframe = pd.read_sql_query(stmt, db.session.bind)
    #return the dataframe as jsonict()
    json_data = dataframe.to_json(orient='records')
    return json_data

@app.route("/winter/<year>/<sport>/vis1")
def winter_dict_ajz(year, sport):
    stmt = db.session.query(Master_data.Year, Master_data.City, Master_data.Sport, Master_data.Discipline, Master_data.Event, Master_data.Gender, Master_data.Country_code, Master_data.Country, Master_data.Medal).\
    filter(Master_data.season == "winter").\
    filter(Master_data.Year == year).\
    filter(Master_data.Sport == sport).\
    statement
    dataframe = pd.read_sql_query(stmt, db.session.bind)
    #return the dataframe as json
    medal_df = pd.DataFrame(dataframe.groupby(['Country','Medal']).count()['Year'])
    medal_df.columns=['Count']
    medal_dict = medal_df.groupby(level=0).apply(lambda df: df.xs(df.name).to_dict()).to_dict()
    return jsonify(medal_dict)

#important
@app.route("/winter/<year>/<sport>/<medal>")
def winter_vis_ajz(year, sport, medal):
    stmt = db.session.query(Master_data.Year, Master_data.City, Master_data.Sport, Master_data.Discipline, Master_data.Event, Master_data.Gender, Master_data.Country_code, Master_data.Country, Master_data.Medal).\
    filter(Master_data.season == "winter").\
    filter(Master_data.Year == year).\
    filter(Master_data.Sport == sport).\
    statement
    dataframe = pd.read_sql_query(stmt, db.session.bind)
    if medal != "Total":
        medal_df = dataframe.loc[dataframe.Medal == medal]
        medal_df = pd.DataFrame(medal_df.groupby('Country').count()['Medal']).sort_values('Medal',ascending=False).reset_index()
        #return the dataframe as json
        json_data = medal_df.to_json(orient='records')
    else:
        medal_df = dataframe
        medal_df = pd.DataFrame(medal_df.groupby('Country').count()['Medal']).sort_values('Medal',ascending=False).reset_index()
        #return the dataframe as json
        json_data = medal_df.to_json(orient='records')
    return json_data

#important
@app.route("/winter/filters")
def winter_filters_ajz():
    """Return lists for filter options"""
    #Year, Sport, Country
    stmt = db.session.query(Master_data.Year, Master_data.City, Master_data.Sport, Master_data.Discipline, Master_data.Event, Master_data.Gender, Master_data.Country_code, Master_data.Country, Master_data.Medal).\
    filter(Master_data.season =="winter").\
    statement
    dataframe = pd.read_sql_query(stmt, db.session.bind)
    years = dataframe.Year.unique().tolist()
    years.sort(reverse=True)
    data = {
        "years": years,
        "sports": dataframe.Sport.unique().tolist()
    }
    return jsonify(data)
    
if __name__ == "__main__":
    app.run()
