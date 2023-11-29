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
engine = create_engine("sqlite:///hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(autoload_with=engine)

# Save references to each table
measurement = Base.classes.measurement
station = Base.classes.station

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
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end><br/>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of dates with precipitation"""
    # Perform a query to retrieve the data and precipitation scores
    one_year_ago = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    prcp_data = session.query(measurement.date, measurement.prcp).\
        filter(measurement.date >= one_year_ago).\
        order_by(measurement.date).all()

    session.close()

    # Convert precipitation list into a dictionary
    prcp_list = []
    for date, prcp in prcp_data:
        prcp_dict = {}
        prcp_dict["date"] = date
        prcp_dict["prcp"] = prcp
        prcp_list.append(prcp_dict)

    # Return a list of jsonified preceipitation for the last 12 months
    return jsonify(prcp_list)

@app.route("/api/v1.0/stations")
def station():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of all stations"""
    # Design a query to calculate the total number of stations in the dataset
    stations = session.query(station.station).all()

    session.close()

    # Convert list of stations into normal list
    station_list = list(np.ravel(stations))

    # Return a list of jsonified stations
    return jsonify(station_list)

@app.route("/api/v1.0/tobs")
def tobs():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of all the total observations"""
    # Using the most active station id
    # Query the last 12 months of temperature observation data for this station and plot the results as a histogram
    one_year_ago = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    most_active = session.query(measurement.date, measurement.tobs).\
        filter(measurement.station == "USC00519281").\
        filter(measurement.date >= one_year_ago).all()

    session.close()

    # Convert temperature observation list into a dictionary
    tobs_list = []
    for date, tobs in most_active:
        tobs_dict = {}
        tobs_dict["date"] = date
        tobs_dict["tobs"] = tobs
        tobs_list.append(tobs_dict)

    # Return a list of jsonified date and temperature observation data for the previous 12 months
    return jsonify(tobs_list)

@app.route("/api/v1.0/<start>")
def start_date(start):
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of min, max, and average of specified start date"""
    start_data = session.query(func.min(measurement.tobs), func.max(measurement.tobs), func.avg(measurement.tobs)).\
        filter(measurement.date >= start).all()

    session.close()

# Convert min, max, and average of specified start date into a dictionary
    start_date_list = []
    for min, max, avg in start_data:
        start_date_dict = {}
        start_date_dict["min"] = min
        start_date_dict["max"] = max
        start_date_dict["avg"] = avg
        start_date_list.append(start_date_dict)

    # Return a list of jsonified min, max, and average of specified start date
    return jsonify(start_date_list)

@app.route("/api/v1.0/<start>/<end>")
def start_end_date(start,end):
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of min, max, and average of specified start date and end date"""
    start_end_data = session.query(func.min(measurement.tobs), func.max(measurement.tobs), func.avg(measurement.tobs)).\
        filter(measurement.date >= start).\
        filter(measurement.date <= end).all()

    session.close()

# Convert min, max, and average of specified start date and end date list into a dictionary
    start_end_date_list = []
    for min, max, avg in start_end_data:
        start_end_date_dict = {}
        start_end_date_dict["min"] = min
        start_end_date_dict["max"] = max
        start_end_date_dict["avg"] = avg
        start_end_date_list.append(start_end_date_dict)

    # Return a list of jsonified min, max, and average of specified start date and end date
    return jsonify(start_end_date_list)

if __name__ == '__main__':
    app.run(debug=True)