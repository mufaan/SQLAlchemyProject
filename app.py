#Import Flask
from flask import Flask, jsonify
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, inspect, desc
from datetime import datetime as DateTime, timedelta as TimeDelta
from datetime import date
from dateutil.parser import parse
import pandas as pd
import numpy as np

# 2. Create an app
app = Flask(__name__)

engine = create_engine("sqlite:///Resources/hawaii.sqlite")
# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

# 3. Define Menu
@app.route("/")
def index():
    return (
		f"/api/v1.0/precipitation<br/>"
		f"/api/v1.0/stations<br/>"
		f"/api/v1.0/tobs<br/>"
        f"/api/v1.0<start>/<end><br/>"
	)

@app.route("/about")
def about():
    name = "Mustafa"
    location = "Houston, TX"

    return f"Hi, my name is {name}, I live in {location}."

@app.route("/precipitation/")
def precipitation():
    session = Session(engine)
    results = session.query(Measurement.date, Measurement.prcp).all()
    
    session.close()
    precipy = list(np.ravel(results))

    return jsonify(precipy)

@app.route("/station/")
def station():
    session = Session(engine)
    results2 =engine.execute('SELECT * FROM station LIMIT 5').fetchall()

    session.close()
    stationlist = list(np.ravel(results2))

    return jsonify(stationlist)

@app.route("/tobs/")
def tobs():
    session = Session(engine)
    results3 =session.query(Station.name, Measurement.station, Station.latitude, Station.longitude, Station.elevation, Measurement.prcp,)\
        .filter(Measurement.date >= '2016-01-30', Measurement.date <= '2017-01-30')\
        .order_by((Measurement.prcp).desc())\
        .all()

    session.close()
    thetemps = list(np.ravel(results3))

    return jsonify(thetemps)

@app.route("/<start>")
def firstoption(start):
    session = Session(engine)
    option1result = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start).all()
    
    session.close()
    option1temp = list(np.ravel(option1result))

    return jsonify(option1temp)


@app.route("/<start>/<end>")
def secondoption(start,end):
    session = Session(engine)
    option2result = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start).filter(Measurement.date <= end).all()
   
    session.close()
    option2temp = list(np.ravel(option2result))
    
    return jsonify(option2temp)


if __name__ == "__main__":
    app.run(debug=True)










