#!/usr/bin/env python
# coding: utf-8

# In[2]:


import pandas as pd
import numpy as np
import datetime as dt

import sqlalchemy 
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify


# In[3]:


engine = create_engine("sqlite:///hawaii.sqlite")

Base = automap_base()
Base.prepare(engine, reflect=True)

Measurement = Base.classes.measurement
Station = Base.classes.station

session = Session(engine)



# In[12]:


app = Flask(__name__)


# In[13]:


@app.route("/")
def welcome():
    return (
        f"Welcome to the Hawaii Climate Analysis API!<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/temp/start/end"
    )


# In[14]:


@app.route("/api/v1.0/precipitation")
def precipitation():
    last_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()
    last_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    
    precipitation = session.querty(Measurement.date, Measurement.prcp).        filter(Measurement.date >= last_year).        order_by(Measurement.date).all()
    
    #{Date, PRCP}
    precip_total = []
    for result in precipitation:
        row = {}
        row["date"] = precipitation[0]
        row["prcp"] = precipitation[1]
        precip_total.append(row)
    return jsonify(precip_total)


# In[15]:


@app.route("/api/v1.0/stations")
def stations():
    results = session.query(Station.station).all()
    
    stattions = list(np.ravel(results))
    return jsonify(stations)


# In[16]:


@app.route("/api/v1.0/tobs")
def temp_monthly():
    last_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()
    last_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    
    prior_temp = session.querty(Measurement.date, Measurement.tobs).        filter(Measurement.date >= last_year).        order_by(Measurement.date).all()
    
    #{Date, PRCP}
    temp_total = []
    for result in precipitation:
        row = {}
        row["date"] = prior_temp[0]
        row["prcp"] = prior_temp[1]
        temp_total.append(row)
    return jsonify(temp_total)


# In[ ]:


@app.route("/api/v1.0/temp/<start>")
@app.route("/api/v1.0/temp/<start>/<end>")
def stats(start=None, end=None):
    sel = [func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]
    if not end:
        results = session.query(*sel).            filter(Measurement.date >= start).all()
        temp = list(np.ravel(results))
        return jsonify(temps)
    
    results = session.query(*sel).        filter(Measurement.date >= start).        filter(Measurement.date <+ end).all()
    temp = list(np.ravel(results))
    return jsonify(temps)

if __name__ == '__main__':
    app.run()


# In[ ]:




