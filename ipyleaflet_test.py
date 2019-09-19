import altair as alt
from data_load_functions import *
# import folium
import geopandas as gpd
# from folium.plugins import MarkerCluster
import numpy as np
from ipyleaflet import Polygon, Map, basemaps, basemap_to_tiles, GeoJSON, MarkerCluster, LayersControl
from ipywidgets import RadioButtons
import json
from viz_funcs import *


if __name__ == '__main__':
    map_dict = get_prepped_dfs()
    structures_map = map_dict['structures']
    m = Map(
        layers=(basemap_to_tiles(basemaps.Esri.WorldTopoMap),),
        center=(60.5, 5),
        zoom=4
    )
    structure_layer = create_layer(structures_map, 'structures',
                                   label_col='steNameEN', secondary_label_col='document',
                                   layer_type='polygon')

    wells = map_dict['wells']
    well_layer = create_layer(wells, 'wells with docs',
                              label_col='wlbWell', secondary_label_col='document',
                              layer_type='marker', filter_on='document', color='red')
    well_layer_no_docs = create_layer(wells, 'wells with docs',
                                      label_col='wlbWell', secondary_label_col='document',
                                      layer_type='marker', filter_on='document', inverse=True, color='gray')

    marker_cluster = MarkerCluster(markers=well_layer.layers, name='Wells with Docs')
    marker_cluster2 = MarkerCluster(markers=well_layer_no_docs.layers, name='Wells without Docs')
    # marker_cluster.add_layer(well_layer)
    m.add_layer(structure_layer)
    m.add_layer(marker_cluster)
    m.add_layer(marker_cluster2)
    m.add_control(LayersControl())
    m
