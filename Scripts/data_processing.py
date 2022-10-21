import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import geopandas as gdp
from pathlib import Path
import plotly.express as px
import sqlite3 as sq
import pandasql as ps
from pyproj import Proj, transform
from conversion import *
import argparse as ap

path = Path.cwd() / 'codepo_gb.gpkg'

data_path = Path.cwd() / 'Electricity_ConsumptionUK.csv'

df = pd.read_csv(data_path)

gdf = gdp.read_file(path)

parser = ap.ArgumentParser(description='Preset values')
parser.add_argument('-a', '--areacode', type=str,metavar='',help='Area code of city', default='CV')
parser.add_argument('-p', '--imagename', type=str,metavar='',help='Insert image name and format', default='image.jpg')
parser.add_argument('-z', '--zoom', type=int,metavar='',help='Zoom +/- in map', default= 7)
parser.add_argument('-n', '--namecsv', type=str,metavar='',help='Input csv name and format', default='electricity.csv')
args = parser.parse_args()

def preprocess_dataframe(df, gdf):
    # Reorder the colums for df and gdf
    cols = ['Postcode', 'Meters', 'Consumption', 'Mean_consumption', 'Median_consumption']
    df.columns = cols
    gdf.loc[:,['Postcode','geometry']]

    # Meging both Uk Energy Consumption and geo DataFrame on the 'Postcode' column 
    merged = df.set_index('Postcode').join(gdf.set_index('Postcode'))

    # finding the number of Null values in geometry column ?
    rows_to_drop = merged[merged['geometry'] == None].index

    # Dropping Null values from merged DataFrame
    merged.drop(rows_to_drop,inplace=True)

    # Creating 2 new columns easting and northing to merged DataFrame
    merged['Eastings'] = 0
    merged['Northings'] = 0

    # Accessing each coordinate in geometry using lambda
    eastings = merged.apply(lambda row: row['geometry'].x,axis=1)
    northings = merged.apply(lambda row: row['geometry'].y,axis=1)

    # Assigning the merged DataFrame Easting column
    merged['Eastings'] = eastings

    #  Assigning the merged DataFrame Northing column
    merged['Northings'] = northings

    # Converting eastings and northing data to longitude and latitudr data for plotly
    vectorized_convert(merged)

    # Dropping unecessary columns in merged DataFrame
    merged = merged.drop(columns=['Meters', 'Consumption', 'geometry', 'Northings', 'Eastings'])

    # Reseting DataFrame
    merged = merged.reset_index()

    return merged


def high_consumers(merged,areacode):
    # Querrying DataFame with SQL with area code
    # sql_query = "Select * from merged where postcode like '@area_code%'"
    # area_consumption = ps.sqldf(sql_query,locals())
    area_consumption = merged.query(f'Postcode.str.contains("{areacode}")', engine='python')

    # Data frame consisting of top consuming house holds in coventry
    area_df = area_consumption[merged['Median_consumption'] > area_consumption['Median_consumption'].quantile(0.99)]

    return area_df


merged = preprocess_dataframe(df,gdf)

# area_code = input("Enter postcode area: ")

region = high_consumers(merged,args.areacode)


def index_to_id(df,file):
    # renaming index column to 'id' and dropping 'index'
    # Resetting DataFrame
    df = df.reset_index()
    
    # renaming index column to 'id'
    df.index.name = 'id'

    # Dropping index column
    df = df.drop(columns=['index']) 

    # Saving .csv of final Data
    df.to_csv(file)

    return df

def plot_high_consumers(area,plot,zoom):
    # plotting high consumers in chosen area
    fig = px.scatter_mapbox(area, lat="latitude", lon="longitude", color="Median_consumption", zoom=zoom, mapbox_style="open-street-map",
                        hover_name="Postcode",hover_data=['Median_consumption'])
    fig = fig.write_image(plot)

    return fig


region_df = index_to_id(region,args.namecsv)

# image = input("Enter imagename.format: ")x 

final_region = plot_high_consumers(region_df,args.imagename,args.zoom)

