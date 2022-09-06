# -*- coding: utf-8 -*-
"""
Created on Sun Jan 10 14:47:05 2021

@author: ppeng
"""
import matplotlib.pyplot as plt
import pandas as pd
import geopandas as gpd

# plt.rcParams.update({'font.size': 16})


#Read the shape file obtained from Census Bureau, the one used in this study was "cb_2018_us_zcta510_500k.shp"
contiguous_usa = gpd.read_file('PATH TO SHAPE FILE')
contiguous_usa.head()
contiguous_usa['ZCTA5CE10']=contiguous_usa['ZCTA5CE10'].astype(int)

# Read in state population data (i.e., population obtained from the Census Bureau)
zip_pop = pd.read_csv('PATH TO ZIPCODE DATA')
zip_pop.head()


# Merge shapefile with zipcode-level data
pop_zips = contiguous_usa.merge(zip_pop, left_on="ZCTA5CE10", right_on="ZCTA5CE10")


#Read and process data for mines obtained from USGS
Au_plants = gpd.read_file ('PATH TO PLANTS')
Au_plants.head()

Au_dfp = gpd.GeoDataFrame(
    Au_plants, geometry=gpd.points_from_xy(Au_plants.LONGITUDE, Au_plants.LATITUDE))

Cu_plants = gpd.read_file ('PATH TO PLANTS')
Cu_plants.head()
Cu_dfp = gpd.GeoDataFrame(
    Cu_plants, geometry=gpd.points_from_xy(Cu_plants.LONGITUDE, Cu_plants.LATITUDE))


Ag_plants = gpd.read_file ('PATH TO PLANTS')
Ag_plants.head()
Ag_dfp = gpd.GeoDataFrame(
    Ag_plants, geometry=gpd.points_from_xy(Ag_plants.LONGITUDE, Ag_plants.LATITUDE))


Al_plants = gpd.read_file ('PATH TO PLANTS')
Al_plants.head()
Al_dfp = gpd.GeoDataFrame(
    Al_plants, geometry=gpd.points_from_xy(Al_plants.LONGITUDE, Al_plants.LATITUDE))

Zn_plants = gpd.read_file ('PATH TO PLANTS')
Zn_plants.head()
Zn_dfp = gpd.GeoDataFrame(
    Zn_plants, geometry=gpd.points_from_xy(Zn_plants.LONGITUDE, Zn_plants.LATITUDE))


#Read and process data for R2-certified recyclers

Recyclers_R2 = gpd.read_file ('PATH TO PLANTS')

Recyclers_R2['LONGITUDE']=Recyclers_R2['LONGITUDE'].astype(float)
Recyclers_R2['LATITUDE']=Recyclers_R2['LATITUDE'].astype(float)

Recyclers_df = gpd.GeoDataFrame(
    Recyclers_R2, geometry=gpd.points_from_xy(Recyclers_R2.LONGITUDE, Recyclers_R2.LATITUDE))


#####Plotting
ax=pop_zips.boundary.plot(linewidth=0.006, color='grey')
pop_zips.plot(ax=ax, color='whitesmoke', legend=True)

##Mines and plants
Au_dfp.plot(ax=ax, marker='^',color="orange",markersize=30, alpha=0.5, label = 'Precious metals')
Ag_dfp.plot(ax=ax, marker='^',color='orange',markersize=30, alpha=0.5 )
Cu_dfp.plot(ax=ax, marker='v',color="royalblue",markersize=30, alpha=0.5, label = 'Base metals (Cu, Zn)')
Al_dfp.plot(ax=ax, marker='D',color='black',markersize=30, alpha=0.5, label = 'Base metals (Al)')
Zn_dfp.plot(ax=ax, marker='v',color='royalblue',markersize=30, alpha=0.5)


###Recyclers
Recyclers_df.plot (ax=ax, markersize=3, color='Green', alpha=0.3, label = 'Recyclers')

ax.set_xlim(-130, -60)
ax.set_ylim(20, 55)
plt.legend(loc='best')
plt.axis('off')
plt.show()
