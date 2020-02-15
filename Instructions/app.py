
## FLASK app for generating Weather data to consumable JSON-ified API ##

import sqlalchemy
import numpy as np
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify

app = Flask(__name__)

## Create an engine to a SQLite database file called `hawaii.sqlite` ##
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the tables
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

#Routes home page
@app.route("/")
def homepage():
    return "Welcome to the webpage"

    # Precipitation route
@app.route("/api/v1.0/precipitation")
def precipitation():
    """ Return a list of measurement date and pricipitation info from 2015 """
    date_prcp_result = session.query(Measurement.date, Measurement.prcp)\
        .filter(Measurement.date >= '2016-08-23').order_by(Measurement.date)
    
    # Creating a dictionary and then appending
    precipation_list =[]
    for p in date_prcp_result:
        prcp_dict = {}
        prcp_dict["date"] = p.date
        prcp_dict["prcp"] = p.prcp
        precipation_list.append(prcp_dict)

    return jsonify(precipation_list)

# return a json list of stations from the dataset

@app.route("/api/v1.0/stations")
def stations():
    """Return a list all station's names"""
    result = session.query(Station.name).all()
    # from tumple to list
    station_names = list(np.ravel(result))
    return jsonify(station_names)

# return a json list of Temperature Observations (tobs) for the previous year
@app.route("/api/v1.0/tobs")
def tobs():
    """Return a list of all temperature observations for the previous year"""
    # Query all tobs values
    result_t = session.query(Measurement.tobs).all()

    # Convert list of tuples into normal list
    tobs_values = list(np.ravel(result_t))

    return jsonify(tobs_values)

#############################################################
# Return a json list of the minimum temperature, the average temperature, and the max 
# temperature for a given start or start-end range.
@app.route("/api/v1.0/<start>")
def temperatures_start(start):
    """ Given the start only, calculate TMIN, TAVG, and TMAX for all dates greater than 
        and equal to the start date. 
    """
    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func\
        .max(Measurement.tobs)).\
                filter(Measurement.date >= start).all()
    
    # Convert list of tuples into normal list
    temperatures_start = list(np.ravel(results))

    return jsonify(temperatures_start)

# When given the start and the end date, calculate the TMIN, TAVG, and TMAX for dates 
# between the start and end date inclusive.
@app.route("/api/v1.0/<start>/<end>")
def temperatures_start_end(start, end):
    """ When given the start and the end date, calculate the TMIN, TAVG, 
        and TMAX for dates between the start and end date inclusive.
    """
    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func\
        .max(Measurement.tobs)).\
                filter(Measurement.date >= start).\
                filter(Measurement.date <= end).all()
    
    # Convert list of tuples into normal list
    temperatures_start_end = list(np.ravel(results))

    return jsonify(temperatures_start_end)

#############################################################

if __name__ == "__main__":
    app.run(debug=True)