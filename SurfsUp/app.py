# Import the dependencies.
import numpy as np
import datetime as dt
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model

Base = automap_base()
# reflect the tables
Base.prepare(autoload_with=engine)

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

#################################################
# Flask Setup
#################################################
app = Flask(__name__)



#################################################
# Flask Routes
#################################################

# home page
@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"Precipiation from the most recent year: /api/v1.0/precipitation<br/>"
        f"All Stations: /api/v1.0/stations<br/>"
        f"Temperature Observations from the Most Active Station in the last year: /api/v1.0/tobs<br/>"
        f"Temperature Observations from a specified start date: /api/v1.0/yyyy-mm-dd<br/>"
        f"Temperature Observations from a specified date range: /api/v1.0/yyyy-mm-dd/yyyy-mm-dd<br/>"
    )


# precipiation route

@app.route("/api/v1.0/precipitation")
def precipitation():

    session = Session(engine)
    date = dt.datetime(2017, 8, 23)
    one_year = dt.date(date.year - 1, date.month, date.day)
    year = session.query(Measurement.date, Measurement.prcp).\
        filter(Measurement.date >= one_year).all()
    session.close()

    precip_dates = []
    for date, precip in year:
        precip_dict = {}
        precip_dict['Date'] = date
        precip_dict['Precipitation'] = precip
        precip_dates.append(precip_dict)
        
    return jsonify(precip_dates)


# stations route

@app.route("/api/v1.0/stations")
def stations():

    session = Session(engine)
    active_stations = session.query(Station.station, Station.name).all()
    session.close()
    
    all_stations = []
    for station, name in active_stations:
        station_dict = {}
        station_dict["Station"] = station
        station_dict["Name"] = name
        all_stations.append(station_dict)
    
    
    return jsonify(all_stations)


# tobs route
@app.route("/api/v1.0/tobs")
def tobs():
    
    session = Session(engine)
    date = dt.datetime(2017, 8, 23)
    one_year = dt.date(date.year - 1, date.month, date.day)
    active_station_last_year = session.query(Measurement.date, Measurement.tobs).\
    filter(Measurement.date >= one_year).\
    filter(Measurement.station == 'USC00519281').all()
    session.close()
    
    active_station_dates = []
    for date, tobs in active_station_last_year:
        active_station_dict = {}
        active_station_dict["Date"] = date
        active_station_dict["Tobs"] = tobs
        active_station_dates.append(active_station_dict)
        
    return jsonify(active_station_dates)



# start route
@app.route("/api/v1.0/<start>")
def start_date(start):
    
    session = Session(engine)
    tobs_data = session.query(func.min(Measurement.tobs), 
                                        func.max(Measurement.tobs), func.avg(Measurement.tobs)).\
    filter(Measurement.date >= start).all()
    session.close()
    
    start_date_tobs = []
    for min, max, avg in tobs_data:
        start_date_dict = {}
        start_date_dict["Min"] = min
        start_date_dict["Max"] = max
        start_date_dict["Average"] = avg
        start_date_tobs.append(start_date_dict)
    
    return jsonify(start_date_tobs)


# start and endroute
@app.route("/api/v1.0/<start>/<end>")
def start_end(start, end):
    
    session = Session(engine)
    tobs_data = session.query(func.min(Measurement.tobs), 
                                        func.max(Measurement.tobs), func.avg(Measurement.tobs)).\
    filter(Measurement.date >= start).\
    filter(Measurement.date <= end).all()
    session.close()
    
    start_end_tobs = []
    for min, max, avg in tobs_data:
        start_end_dict = {}
        start_end_dict["Min"] = min
        start_end_dict["Max"] = max
        start_end_dict["Average"] = avg
        start_end_tobs.append(start_end_dict)
    
    
    return jsonify(start_end_tobs)










################# Run ################

if __name__ == '__main__':
    app.run(debug=True)




















