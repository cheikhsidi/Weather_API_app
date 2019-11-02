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
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station

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
        f"Welcome to My Flask App<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start/<start><br/>"
        f"/api/v1.0/start/end/<start>/<end>"
    )


@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return the JSON representation of your dictionary"""
    # Query all precipitations
    results = session.query(Measurement.date, Measurement.prcp).all()
    
    session.close()

    # Convert list of tuples into normal list
    all_Precipitation = []
    for date, prcp in results:
        prcp_dict = {}
        prcp_dict["date"] = date
        prcp_dict["prcp"] = prcp
        all_Precipitation .append(prcp_dict)
    

    return jsonify(all_Precipitation)


@app.route("/api/v1.0/stations")
def station():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a JSON list of stations from the dataset"""
    # Query all Stations
    results = session.query(Station.name).all()

    session.close()


    stations = list(np.ravel(results))
    return jsonify(stations)


@app.route("/api/v1.0/tobs")
def tobs():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a JSON list of Temperature Observations (tobs) for the previous year"""
    # Query all Temperatures
    last_12 = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    Temp_scores = session.query(Measurement.date, Measurement.tobs).\
        filter(Measurement.date > last_12).all()

    session.close()
    

    tobs = list(np.ravel(Temp_scores))
    return jsonify(tobs)

@app.route("/api/v1.0/start/<start>")
def start(start):
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start or start-end range"""
    # Query all Temperatures
    results = session.query(Measurement.date, func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start).\
        group_by(Measurement.date).all()

    session.close()
    f"Please Enter the start date for your trip"

    # Convert list of tuples into normal list
    #temperture_stat = []
    for date, tmin, tavg, tmax in results:
        prcp_dict = {}
        prcp_dict["date"] = date
        prcp_dict["Temp_Min"] = tmin
        prcp_dict["Temp_avg"] = tavg
        prcp_dict["Temp_max"] = tmax

    temperture_stat = list(results)


    return jsonify(temperture_stat)


@app.route("/api/v1.0/start/end/<start>/<end>")
def end(start, end):
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start or start-end range"""
    # Query all Temperatures
    results = session.query(Measurement.date, func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start).\
        filter(Measurement.date <= end).group_by(Measurement.date).all()

    session.close()

    # Convert list of tuples into normal list
    #temperture_stat = []
    # for date, tmin, tavg, tmax in results:
    #     prcp_dict = {}
    #     prcp_dict["date"] = date
    #     prcp_dict["Temp_Min"] = tmin
    #     prcp_dict["Temp_avg"] = tavg
    #     prcp_dict["Temp_max"] = tmax

    temperture_stat = list(results)

    return jsonify(temperture_stat)

if __name__ == '__main__':
    app.run(debug=True)
