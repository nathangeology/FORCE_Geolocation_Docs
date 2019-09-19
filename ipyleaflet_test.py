import os
os.path.join('/home/nathanieljones/PycharmProjects/FORCE_Geolocation_Docs/')
import altair as alt
from data_load_functions import *
import folium
import geopandas as gpd
from folium.plugins import MarkerCluster
import numpy as np
from ipyleaflet import Polygon, Map, basemaps, basemap_to_tiles, GeoJSON
from ipywidgets import RadioButtons
import json
from viz_funcs import *

if __name__ == '__main__':
    map_dict = create_npd_shapefile_dict()
    structures_map = map_dict['structures']
    structure_layer = create_layer(structures_map, 'structures', layer_type='polygon')
    # filter_list = []
    # for idx, row in structures_map.iterrows():
    #     if row['geometry'] is None:
    #         filter_list.append(False)
    #     elif str(type(row['geometry'])) == '<class \'shapely.geometry.multipolygon.MultiPolygon\'>':
    #         filter_list.append(False)
    #     else:
    #         filter_list.append(True)
    # structures_map = structures_map[filter_list]
    # structures_map = structures_map.to_crs(epsg=4326)
    # structures_map.to_file("structures.geojson", driver='GeoJSON')
    m = Map(
        layers=(basemap_to_tiles(basemaps.CartoDB.DarkMatter),),
        center=(60.5, 5),
        zoom=4
    )
    filter_list = []
    for idx, row in structures_map.iterrows():
        if row['geometry'] is None:
            filter_list.append(False)
        elif str(type(row['geometry'])) == '<class \'shapely.geometry.multipolygon.MultiPolygon\'>':
            filter_list.append(False)
        else:
            filter_list.append(True)
    structures_map = structures_map[filter_list]
    structures_map = structures_map.to_crs(epsg=4326)
    structures_map.to_file("structures.geojson", driver='GeoJSON')
    m = Map(
        layers=(basemap_to_tiles(basemaps.Esri.NatGeoWorldMap),),
        center=(60.5, 5),
        zoom=4
    )
    # for _, polygon in structures_map.iterrows():
    #     current
    with open("structures.geojson", 'r') as f:
        structure_data = json.load(f)
    structure_layer2 = GeoJSON(data=structure_data,
                              style={'color': 'green', 'opacity': 1, 'weight': 1.9, 'dashArray': '9',
                                     'fillOpacity': 0.1})
    # for _, polygon in structures_map.iterrows():
    #     current
    # with open("structures.geojson", 'r') as f:
    #   structure_data = json.load(f)
    # structures =  GeoJSON(data=structure_data , style = {'color': 'green', 'opacity':1, 'weight':1.9, 'dashArray':'9', 'fillOpacity':0.1})
    m.add_layer(structure_layer)
