
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

if __name__ == "__main__":
    app.run(debug=True)