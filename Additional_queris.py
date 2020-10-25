# Dependencies
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt    

# Python SQL toolkit and Object Relational Mapper
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

engine = create_engine("sqlite:///hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(engine, reflect=True)

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

#  Import the sqlalchemy extract function.
from sqlalchemy import extract

#   Check the temperatures for June and December for all datapoints 

J_temp= session.query(Measurement.date,Measurement.tobs).filter(extract('month', Measurement.date) == 6).all()
J_temp_df = pd.DataFrame(J_temp,columns=['date','June temperature']).sort_index()
J_temp_df = J_temp_df.groupby(J_temp_df['date'].str.slice(0,4)).mean()


D_temp = session.query(Measurement.date,Measurement.tobs).filter(extract('month', Measurement.date) == 12).all()
D_temp_df = pd.DataFrame(D_temp,columns=['date','December temperature'])
D_temp_df = D_temp_df.groupby(D_temp_df['date'].str.slice(0,4)).mean()

#print(J_temp_df)



plotdata = pd.DataFrame({
  "June temperatures" : J_temp_df['June temperature'],
  "December temperatures" : D_temp_df['December temperature']}
  ,index = J_temp_df.index)

plotdata.plot(kind="bar",title="Oahu average temperatures over years",ylim=[50,90])
plt.xlabel('year')
plt.ylabel('average temperature')

plt.show()

J_prcp = session.query(Measurement.date,Measurement.prcp).filter(extract('month', Measurement.date) == 6).all()
J_prcp_df = pd.DataFrame(J_prcp,columns = ['date','June precipitation']).sort_index()
J_prcp_df = J_prcp_df.groupby(J_prcp_df['date'].str.slice(0,4)).mean()

D_prcp = session.query(Measurement.date,Measurement.prcp).filter(extract('month', Measurement.date) == 12).all()
D_prcp_df = pd.DataFrame(D_prcp,columns = ['date','December precipitation'])
D_prcp_df = D_prcp_df.groupby(D_prcp_df['date'].str.slice(0,4)).mean()


plotdata = pd.DataFrame({
    "June precipitations" : J_prcp_df['June precipitation'],
    "December precipitations" : D_prcp_df['December precipitation']}
    ,index = J_prcp_df.index)

plotdata.plot(kind="bar",title="Oahu average precipitations over years")
plt.xlabel('year')
plt.ylabel('average precipitation')

plt.show()