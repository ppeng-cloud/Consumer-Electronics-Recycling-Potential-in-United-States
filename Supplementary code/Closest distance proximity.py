# -*- coding: utf-8 -*-
"""
Created on Fri Dec 31 11:33:59 2021

@author: ppeng
"""


import geopandas as gpd
import numpy as np
import pandas as pd
import openpyxl as openpyxl
import matplotlib.pyplot as plt
from scipy.spatial import cKDTree
from shapely.geometry import Point


# Read the shape file for zip-code level mappting, which could be obtained from Census Bureau. The one used in this study was "cb_2018_us_zcta510_500k.shp"

contiguous_usa = gpd.read_file('FILE PATH')
contiguous_usa.head()
contiguous_usa['ZCTA5CE10']=contiguous_usa['ZCTA5CE10'].astype(int)

# Read in state population data and examine
zip_pop = pd.read_csv('FILE PATH')
zip_pop.head()



# Merge shapefile with population data
pop_zips = contiguous_usa.merge(zip_pop, left_on="ZCTA5CE10", right_on="ZCTA5CE10")


#Load the csv file that contain geospatial data for the target plant
NV_plant = gpd.read_file ('FILE PATH')
NV_plant.head()


NV_dfp = gpd.GeoDataFrame(
    NV_plant, geometry=gpd.points_from_xy(NV_plant.LONGITUDE, NV_plant.LATITUDE))

pop_screen = pop_zips.copy()  #Create an arbitrary variable for screening
pop_screen['geometry'] = pop_screen['geometry'].centroid

gpd1=pop_screen


def ckdnearest(gdA, gdB):   ##Credit: JHuw and Ric S @Stackexchange 

    nA = np.array(list(gdA.geometry.apply(lambda x: (x.x, x.y))))
    nB = np.array(list(gdB.geometry.apply(lambda x: (x.x, x.y))))
    btree = cKDTree(nB)
    dist, idx = btree.query(nA, k=1)
    gdB_nearest = gdB.iloc[idx].drop(columns="geometry").reset_index(drop=True)
    gdf = pd.concat(
        [
            gdA.reset_index(drop=True),
            gdB_nearest,
            pd.Series(dist, name='dist')
        ], 
        axis=1)

    return gdf


shorted_dis_NV = ckdnearest(gpd1, NV_dfp)

#You should get the zip codes that have the closest straight line distance with the target plant. 


