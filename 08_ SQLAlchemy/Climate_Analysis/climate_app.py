import numpy as np
import pandas as pd
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
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)


#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################


@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/><br/>"
        f"/api/v1.0/precipitation<br/>"
        f"Returns a JSON list of percipitation data for the last 12 months<br/><br/>"
        f"/api/v1.0/stations<br/>"
        f"Return a JSON list of stations<br/><br/>"
        f"/api/v1.0/tobs<br/>"
        f"Return a JSON list of Temperature Observations (tobs) for the last 12 months<br/><br/>"
        f"/api/v1.0/start<br/>"
        f"Return a JSON list of the MIN/AVG/MAX temperature for a given start date (YYYY-MM-DD)<br/><br/>"
        f"/api/v1.0/start/end<br/>"
        f"Return a JSON list of the MIN/AVG/MAX temperature for a given start-end range (YYYY-MM-DD)<br/><br/>"
    )


@app.route("/api/v1.0/precipitation")
def precipitation():
    """Returns a JSON list of percipitation data for the last 12 months"""

    # Query to pull last 12 months   
    last_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()[0]
    start_date = dt.date(2017, 8, 23) - dt.timedelta(days=365)

    # Query to pull precipitation scores 
    prcp_results = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= start_date).\
        order_by(Measurement.date).all()

    # Create a dictionary from the row data and append to a list of all_prcp
    all_prcp = []
    for date, prcp in prcp_results:
        prcp_dict = {}
        prcp_dict["date"] = date
        prcp_dict["prcp"] = prcp
        all_prcp.append(prcp_dict)

    return jsonify(all_prcp)
    

@app.route("/api/v1.0/stations")
def stations():
    """Return a JSON list of stations from the dataset"""

    # Query all stations
    station_results = session.query(Station.station, Station.latitude, Station.longitude,
    Station.name, Station.id, Station.elevation).all()

    # Create a dictionary from the row data and append to a list of all_stations
    all_stations = []
    for station, latitude, longitude, name, id, elevation in station_results:
        station_dict = {}
        station_dict["station"] = station
        station_dict["latitude"] = latitude
        station_dict["longitude"] = longitude
        station_dict["name"] = name
        station_dict["id"] = id
        station_dict["elevation"] = elevation
        all_stations.append(station_dict)

    return jsonify(all_stations)


@app.route("/api/v1.0/tobs")
def tobs():
    """Return a JSON list of Temperature Observations (tobs) for the last 12 months"""

    # Query to pull last 12 months    
    last_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()[0]
    start_date = dt.date(2017, 8, 23) - dt.timedelta(days=365)

    # Query to pull temperature observations
    temp_results = session.query(Measurement.date, Measurement.tobs).filter(Measurement.date >= start_date).\
        order_by(Measurement.date).all()
    
    # Create a dictionary from the row data and append to a list of all_tobs
    all_tobs = []
    for date, tobs in temp_results:
        tobs_dict = {}
        tobs_dict["date"] = date
        tobs_dict["tobs"] = tobs
        all_tobs.append(tobs_dict)

    return jsonify(all_tobs)


@app.route("/api/v1.0/<start>")
def start_date_only(start=None):
    """Return a JSON list of the MIN/AVG/MAX temperature for a given start date (YYYY-MM-DD)"""

    # Query to calculate TMIN, TAVG, and TMAX for all dates greater than and equal to start date
    start_results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs),
    func.max(Measurement.tobs)).filter(Measurement.date >= start).all()

    # Create a list of dictionary with MIN/AVG/MAX temperature for start date
    all_start_date = []
    for tmin, tavg, tmax in start_results:
        start_dict = {}
        start_dict["minimum temperature"] = tmin
        start_dict["average temperature"] = tavg
        start_dict["max temperature"] = tmax
        all_start_date.append(start_dict)

    return jsonify(all_start_date)
    

@app.route("/api/v1.0/<start>/<end>")
def start_end_date(start=None,end=None):
    """Return a JSON list of the MIN/AVG/MAX temperature for a given start-end range (YYYY-MM-DD)"""

    #Query to calculate the TMIN, TAVG, and TMAX for dates between the start and end date inclusive.
    start_end_results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs),
    func.max(Measurement.tobs)).filter(Measurement.date >= start).filter(Measurement.date <= end).all()

    # Create a list of dictionary with MIN/AVG/MAX temperature for start date
    all_start_end = []
    for tmin, tavg, tmax in start_end_results:
        startend_dict = {}
        startend_dict["minimum temperature"] = tmin
        startend_dict["average temperature"] = tavg
        startend_dict["max temperature"] = tmax
        all_start_end.append(startend_dict)

    return jsonify(all_start_end)


if __name__ == '__main__':
    app.run(debug=True)