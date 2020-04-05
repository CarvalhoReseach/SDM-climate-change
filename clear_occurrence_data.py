#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov 15 17:19:36 2019

@authors: Carlos Eduardo de Carvalho, Francisca Soares de Araújo, Julia Caram Sfair
"""

"""
Description:
    This script as developed in context of project entitled EFEITO DAS MUDANÇAS 
    CLIMÁTICAS NA DISTRIBUIÇÃO DE PLANTAS COM DIFERENTES ESTRATÉGIAS DE 
    USO DE ÁGUA.
"""

#==============================================================================
'''                     Usual Python Libraries                           '''

#import shapefile as shp
#from glob import glob
import pandas as pd
#import rasterio
#import matplotlib.pyplot as plt
#import matplotlib as mpl
#import cmocean
#import numpy as np
#import time
#from matplotlib.colors import ListedColormap, BoundaryNorm
#from matplotlib.patches import Patch
import geopandas as gpd
import rasterstats as rs
#import seaborn as sns; 
#import gdal
#sns.set(font_scale=1.5)
#plt.style.use('fivethirtyeight')
#==============================================================================

def gbif_csv_to_geodataframe(csv_name):
    """
    Read a gbif csv in darwincore format and transform in geodataframe
    using decimalLongitude and decimalLatitude columns
    
    use exemple: 
        data = gbif_csv_to_geodataframe('/home/user/zizyphus_joazeiro.csv')
        
    Parameters
    ----------
    csv_name : str
            path to csv table
    """
    data=pd.read_csv(csv_name,sep='\t') 
    data = gpd.GeoDataFrame(data,geometry=gpd.points_from_xy(x=data.decimalLongitude,y=data.decimalLatitude))
    return data

def remove_null_coordinates(points_dataframe):
    """
    Delete line without coordinates in column geometry ex: POINT (nan nan).
    function requires points in geodataframe format
    
    use exemple:
        data = gbif_csv_to_geodataframe('/home/user/zizyphus_joazeiro.csv')
        
        null_removed = remove_null_coordinates(data)
    
    Parameters
    ----------
    points_dataframe : geopandas.geodataframe.GeoDataFrame
            A geodataframe with points of species occurrence
    """
    points_dataframe=points_dataframe[pd.notnull(points_dataframe['decimalLatitude'])]
    points_dataframe=points_dataframe[pd.notnull(points_dataframe['decimalLongitude'])]    
    return points_dataframe

def remove_out_geometry_points(points_dataframe,boundary):
    """
    This function remove lines with outlier points (e.g. outside the known range of the species, 
    occurrences in water for terrestrial species or occurrences in earth for aquatic species )
    
    use exemple:
        zizyphus_joazeiro = gbif_csv_to_geodataframe('/home/user/zizyphus_joazeiro.csv')
        
        remove_out_geometry_points = (zizyphus_joazeiro,'/home/user/world.shp')
    
    Parameters
    ----------
    points_dataframe : geopandas.geodataframe.GeoDataFrame
            A geodataframe with points of species occurrence
    
    boundary : str
            path to shapefile with area filter (e.g. ocean, continent or specie known range )
    """
   
    boundary=gpd.read_file(boundary) 
    boundary=boundary.geometry.unary_union    
    points_clip = points_dataframe[points_dataframe.geometry.intersects(boundary)] 
    return points_clip
   
def compute_road_distance(points_dataframe, roads):
    """
    This function compute distance between point occurrence and lines as roads shapefile.
    The EPSG of two data  must be epsg:4326 that is WGS84 Datum and coordinates in decimal format.
    The distance in meters from the shapefile road is saved in the "dist" column of the 
    geodataframe.

    use exemple:
        zizyphus_joazeiro = gbif_csv_to_geodataframe('/home/user/zizyphus_joazeiro.csv')
        
        compute_road_distance = (zizyphus_joazeiro,'/home/user/roads.shp')
    
    Parameters
    ----------
    points_dataframe : geopandas.geodataframe.GeoDataFrame
            A geodataframe with points of species occurrence
    
    roads : str
            path to shapefile roads
            
    """
    roads = gpd.read_file(roads)
    roads.crs = {'init' :'epsg:4326'}
    roads=roads.to_crs({'init': 'epsg:3395'})
    roads=roads.geometry.unary_union
    points_dataframe.crs = {'init' :'epsg:4326'}
    points_dataframe=points_dataframe.to_crs({'init': 'epsg:3395'})
    points_dataframe['dist']=points_dataframe.geometry.distance(roads).values
    points_dataframe = points_dataframe.to_crs({'init': 'epsg:3395'})    
    
    return points_dataframe

def sample_raster_with_points(points_dataframe,raster,dataset=None,raster_type='categorical'):
    """
    This function sample value of enviromental variable in coordinates of specie ocurrence. 
    For example, elevation in specific coordinates.

    use exemple:
        zizyphus_joazeiro = gbif_csv_to_geodataframe('/home/user/zizyphus_joazeiro.csv')
        
        species_elevation = sample_raster_with_points(zizyphus_joazeiro, '/home/user/elevation.tif', dataset='elevation', raster_type='continuous')
        
    Parameters
    ----------
    points_dataframe : geopandas.geodataframe.GeoDataFrame
            A geodataframe with points of species occurrence
    
    raster : str
        Path to raster dataset
    dataset : str
            Name of dataset for white a column with values
    raster_type : categorical or continuous
    
    """
    
    if raster_type != 'categorical':
        sample = [rs.point_query(i,raster,interpolate='bilinear')[0] for i in points_dataframe.geometry]
    else:
        sample = [rs.point_query(i,raster,interpolate='nearest')[0] for i in points_dataframe.geometry]
    points_dataframe[dataset]=sample
    return points_dataframe
    

    
    












