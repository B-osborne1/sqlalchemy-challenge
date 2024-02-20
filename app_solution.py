# Import the dependencies.
import numpy as np
import pandas as pd
import datetime as dt

# Python SQL toolkit and Object Relational Mapper

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine

from flask import Flask, jsonify
# 2. Create an app, being sure to pass __name__
app = Flask(__name__)

#################################################
# Database Setup
#################################################
# Create engine using the `hawaii.sqlite` database file
engine = create_engine("sqlite:///Resources/hawaii.sqlite")
# Declare a Base using `automap_base()`
Base = automap_base()
# Use the Base class to reflect the database tables
Base.prepare(autoload_with=engine)

# Assign the measurement class to a variable called `Measurement` and
# the station class to a variable called `Station`
Measurement = Base.classes.measurement
Station = Base.classes.station



#################################################
# Flask Routes
#################################################
@app.route("/")
def home():
    return (f"Welcome! The following extensions are available:<br/><br/>"
            f"To see Hawaii's precipitation: /api/v1.0/precipitation<br/>"
            f"To find a list of Hawaii's weather stations: /api/v1.0/stations<br/>"
            f"To find the latest year of weather: /api/v1.0/tobs<br/><br/>"
            f"Still to be added:<br/>"
            f"Finding the temp data from any point until most recent: /api/v1.0/<start><br/>"
            f"Finding the temp data from any range: /api/v1.0/<start>/<end>")


#Precipitation by date
@app.route("/api/v1.0/precipitation")
def prcp():
    #Connecting to SQL
    session = Session(engine)
    precipitation_dict = {}
    precipitation_data = session.query(Measurement).all()

    #Creating DF of date and precipitation
    precipitation_df = pd.DataFrame([(data.date, data.prcp) for data in precipitation_data], columns=['Date', 'Precipitation'])
    precipitation_df = precipitation_df.sort_values(by='Date', ascending=True)

    #Creating dictionary
    for index, row in precipitation_df.iterrows():
        date = row['Date']
        precipitation = row['Precipitation']
        precipitation_dict[date] = precipitation

    return jsonify(precipitation_dict)
    session.close()

#Station list
@app.route("/api/v1.0/stations")
def stat():
    #Connecting to SQL
    session = Session(engine)
    measurement_data = session.query(Measurement).all()
    
    #Creating DF for stations
    stations = pd.DataFrame([data.station for data in measurement_data], columns=['Station'])
    
    #Getting value counts for occurence of each station
    station_counts = stations['Station'].value_counts().reset_index()
    station_counts.columns = ['Station', 'Count']
    
    #Transferring information into a json format
    stations_json = station_counts.to_json(orient='values')
    
    return stations_json
    session.close()

    return print(stations_json)

#Temperature for last 365 days
@app.route("/api/v1.0/tobs")
def tobs():
    #Connect to SQL
    session = Session(engine)
    #Outline timeframe
    year_ago = dt.datetime(2017, 8, 23) - dt.timedelta(days=365)
    #Isolate values from specific station
    temp_top = session.query(Measurement).filter(Measurement.date >= year_ago, Measurement.station == 'USC00519281').all()
    temp_top_df = pd.DataFrame([(data.date, data.tobs) for data in temp_top], columns=['Date', 'Temperature'])
    temp_top_df = temp_top_df.sort_values(by='Date', ascending=True)
    
    temp_dict = {}
    #Create dictionary for json use
    for index, row in temp_top_df.iterrows():
        date = row['Date']
        temperature = row['Temperature']
        temp_dict[date] = temperature

    return jsonify(temp_dict)
    session.close()

#TBC
@app.route("/api/v1.0/<start>")
def start():
    return ""

@app.route("/api/v1.0/<start>/<end>")
def all():
    return ""

#Closing code
if __name__ == "__main__":
    app.run(debug=True)
