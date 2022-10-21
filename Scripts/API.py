from flask import Flask, render_template, request
from flask_wtf import FlaskForm
from dotenv import load_dotenv
from wtforms import SelectField, SubmitField
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, MetaData
from sqlalchemy import Column, Integer, Text, Float, REAL, String
import plotly.express as px
import pandas as pd
from plotly.offline import plot
import os
import os.path
import yaml


# Loading .env file
load_dotenv('.env')
config_secret_key = os.getenv('SECRET_KEY')

# BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# db_path = os.path.join(BASE_DIR, "energy.db")


app = Flask(__name__)
app.config["DEBUG"] = True
app.config['SECRET_KEY'] = config_secret_key
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///ukenergy.sqlite"
# app.config['SQLALCHEMY_TRACK_MODIFICATION'] = True 
# db = SQLAlchemy(app)
# migrate = Migrate(app, db)

DATABASE_URL = os.getenv('DATABASE_URL')

engine = create_engine(DATABASE_URL, echo=True, connect_args={'check_same_thread': False})
session = Session(engine)

metadata = MetaData()
metadata.reflect(engine)


Base = automap_base(metadata=metadata)

# pre-declare User for the 'user' table
class User(Base):
    __tablename__ = 'UKEnergy'

    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True)
    Areacode = Column(String)
    Postcode = Column(Text)
    Mean_consumption = Column(Float)
    Median_consumption = Column(Float)
    Longitude = Column(REAL)
    Latitude = Column(REAL)

    def to_dict(self):
        return {
            'id': self.id,
            'Areacode': self.Areacode,
            'Postcode': self.Postcode,
            'Mean_consumption': self.Mean_consumption,
            'Median_consumption': self.Median_consumption,
            'Longitude': self.Longitude,
            'Latitude': self.Latitude
        }

with app.app_context():
    Base.prepare(engine,reflect=True)


@app.route('/get')
def servery():
    form = ASelectForm()
    results = session.query(User).filter(User.Postcode.like("CV%"))
    for r in results:
        print(r)
        break
    return ''

areacode_selection = ''

@app.route('/query', methods= ["POST"])
def server():
    # Assigning global vaiable to selected areacodes from form
    global areacode_selection
    areacode_selection  = request.form.get('select')

    #Plotting
    query2 = session.query(User).filter(User.Postcode.like(f'{areacode_selection}%'))
    query3 = [user.to_dict() for user in query2]
    df = pd.DataFrame(query3)

    fig = px.scatter_mapbox(df, lat="Latitude", lon="Longitude", color="Median_consumption", zoom=5, mapbox_style="open-street-map",
                        hover_name="Postcode",hover_data=['Median_consumption'])

    div = fig.to_html(full_html=False)

    return render_template('server_table.html', title='UK Electricity Consumption 2021',fig=div)

@app.route('/input/query/')
def query_user():
    
    query2 = session.query(User).filter(User.Postcode.like(f'{areacode_selection}%'))

    # Filter search
    search = request.args.get('search[value]')
    if search:
        query2 = query2.filter(User.Postcode.like(f'%{search}%'))
    total_filtered = query2.count()
    
    # Pagination
    start = request.args.get('start', type=int)
    length = request.args.get('length', type=int)
    query2 = query2.offset(start).limit(length)
    
    return {
        'data': [user.to_dict() for user in query2], 
        'recordsFiltered': total_filtered,
        'recordsTotal': session.query(User).count(),
        'draw': request.args.get('draw', type=int)
    }

# Calling .yaml file containing list of postcodes
with open("config.yaml","r") as file:
    area_code = yaml.safe_load(file)

# Create a form class
class ASelectForm(FlaskForm):
    city_areacode = SelectField('Select your areacode', choices=area_code)
    Submit_areacode = SubmitField("Submit")


@app.route('/', methods=['GET', 'POST'])
@app.route('/input', methods=['GET', 'POST'])

def input():

    form = ASelectForm()
    
    areacode = form.city_areacode
    form.city_areacode.data = ''

    return render_template('input.html',areacode=areacode, form=form)

app.run(port=7777)