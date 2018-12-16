import pandas as pd
import sqlalchemy
import pymysql
pymysql.install_as_MySQLdb()
import flask
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly
from flask import Flask
from flask_cors import CORS, cross_origin
from flask import Flask, jsonify, render_template

database_username = 'root'
database_password = '060415Pame$'
database_ip       = '127.0.0.1:3306'
database_name     = 'olympics'
database_connection = sqlalchemy.create_engine('mysql+mysqlconnector://{0}:{1}@{2}/{3}'.
                                              format(database_username, database_password,
                                                     database_ip, database_name))
                                                     
df = pd.read_sql_table('master_data', con=database_connection)

json_data = df.to_json(orient='records')



usa = df.loc[df['Country_code'] == 'USA']
#Usa Gold DataFrame
usa_gold = usa.loc[df['Medal'] == 'Gold']
#Usa Gold for Plot.ly
usa_gold_chart = usa_gold.loc[:, ["Medal"]].count()
usa_gold_chart
#in order to plot the variable find the Key, which is medal in this case 
dash_usa_gold = usa_gold_chart['Medal']
dash_usa_gold
#Usa Silver DataFrame
usa_silver = usa.loc[df['Medal'] == 'Silver']
#Usa Silver for Plot.ly
usa_silver_chart = usa_silver.loc[:, ["Medal"]].count()
usa_silver_chart
#in order to plot the variable find the Key, which is medal in this case 
dash_usa_silver = usa_silver_chart['Medal']
dash_usa_silver
#Usa Bronze DataFrame
usa_bronze = usa.loc[df['Medal'] == 'Bronze']
#Usa bronze for Plot.ly
usa_bronze_chart = usa_bronze.loc[:, ["Medal"]].count()
usa_bronze_chart
#in order to plot the variable find the Key, which is medal in this case 
dash_usa_bronze = usa_bronze_chart['Medal']
dash_usa_bronze



#Rus DataFrame
rus= df.loc[df['Country_code'] == 'RUS'] 
#Rus Gold DataFrame
rus_gold = rus.loc[df['Medal'] == 'Gold']
#Rus Gold for Plot.ly
rus_gold_chart = rus_gold.loc[:, ["Medal"]].count()
rus_gold_chart
#in order to plot the variable find the Key, which is medal in this case 
dash_rus_gold = rus_gold_chart['Medal']
dash_rus_gold
#Rus Silver DataFrame
rus_silver = rus.loc[df['Medal'] == 'Silver']
#Rus Silver for Plot.ly
rus_silver_chart = rus_silver.loc[:, ["Medal"]].count()
rus_silver_chart
#in order to plot the variable find the Key, which is medal in this case 
dash_rus_silver = rus_silver_chart['Medal']
dash_rus_silver
#Rus bronze DataFrame, 
rus_bronze = rus.loc[df['Medal'] == 'Bronze']
#Rus bronze for Plot.ly
rus_bronze_chart = rus_bronze.loc[:, ["Medal"]].count()
rus_bronze_chart
#in order to plot the variable find the Key, which is medal in this case 
dash_rus_bronze = rus_bronze_chart['Medal']
dash_rus_bronze


#Total Medal Count entire data set 
df.loc[:, ["Country_code", "Medal"]].count()


#Total Usa Medal Count 
usa_medal = usa.loc[:, ["Medal"]]
usa_medal.count()

#Total Rus Medal Count 
rus_medal = rus.loc[:, ["Medal"]]
rus_medal.count()

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

# cors = CORS(app)
# app.config['CORS_HEADERS'] = 'Content-Type'

colors = {
    'background': '#F5EAFE',
    'text': '#131313'
}


app.layout = html.Div(children=[
    html.H1(children='Olympic Medals, 1896-2014'),

    html.Div(children='''
        Dash: The summer and winter medal count between two nations.
    '''),

    dcc.Graph(
        id='example-graph',
        figure={
            'data': [
                {'x': ['Gold', 'Silver', 'Bronze'], 'y': [dash_usa_gold, dash_usa_silver, dash_usa_bronze], 'type': 'bar', 'name': 'USA'},
                {'x': ['Gold', 'Silver', 'Bronze'], 'y': [dash_rus_gold, dash_rus_silver, dash_rus_bronze], 'type': 'bar', 'name': u'RUSSIA'},
            ],
            'layout': {
                'title': 'America vs. Russia'
                
            }
        }
    )
])
    
    






if __name__ == "__main__":
    app.run_server(debug=True)