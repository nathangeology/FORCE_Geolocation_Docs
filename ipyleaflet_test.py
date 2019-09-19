import altair as alt
from data_load_functions import *
# import folium
import geopandas as gpd
# from folium.plugins import MarkerCluster
import numpy as np
from ipyleaflet import Polygon, Map, basemaps, basemap_to_tiles, GeoJSON, MarkerCluster, LayersControl, FullScreenControl
from ipywidgets import RadioButtons
import json
from viz_funcs import *
import pickle


if __name__ == '__main__':
    file_path = "joined_dfs.pkl"
    with open(file_path, "rb") as f:
        final_dataframe = pickle.load(f)
    check_cols = list(final_dataframe.columns[-9:])
    map_dict = get_prepped_dfs()
    structures_map = map_dict['structures']
    fields_map = map_dict['fields']
    blocks_map = map_dict['blocks']
    subareas_map = map_dict['sub_areas']
    discoveries_map = map_dict['discoveries']
    facilities_map = map_dict['facilities']
    m = Map(
        layers=(basemap_to_tiles(basemaps.Esri.WorldTopoMap),),
        center=(60.5, 5),
        zoom=4,
        figsize=(10, 15)
    )
    structure_layer = create_layer(structures_map, 'structures',
                                   label_col='steNameEN', secondary_label_col='document',
                                   layer_type='polygon', filter_on='document', inverse=True, color='lightGray')
    structure_layer_docs = create_layer(structures_map, 'structures_docs',
                                        label_col='steNameEN', secondary_label_col='document',
                                        layer_type='polygon', filter_on='document', color='orange')
    fields_layer = create_layer(fields_map, 'fields',
                                label_col='FIELDNAME', secondary_label_col='document',
                                layer_type='polygon', filter_on='document', inverse=True, color='lightGray')
    fields_layer_docs = create_layer(fields_map, 'fields_docs',
                                     label_col='FIELDNAME', secondary_label_col='document',
                                     layer_type='polygon', filter_on='document', color='red')
    subareas_layer = create_layer(subareas_map, 'subareas',
                                  label_col='NAME', secondary_label_col='document',
                                  layer_type='polygon', filter_on='document', inverse=True, color='lightGray')
    subareas_layer_docs = create_layer(subareas_map, 'subareas_docs',
                                       label_col='NAME', secondary_label_col='document',
                                       layer_type='polygon', filter_on='document', color='blue')
    discoveries_layer = create_layer(discoveries_map, 'discoveries',
                                     label_col='DISCNAME', secondary_label_col='document',
                                     layer_type='polygon', filter_on='document', inverse=True, color='lightGray')
    discoveries_layer_docs = create_layer(discoveries_map, 'discoveries_docs',
                                          label_col='DISCNAME', secondary_label_col='document',
                                          layer_type='polygon', filter_on='document', color='green')
    facilities_layer = create_layer(facilities_map, 'facilities',
                                    label_col='FACNAME', secondary_label_col='document',
                                    layer_type='marker', filter_on='document', inverse=True, color='lightGray')
    facilities_layer_docs = create_layer(facilities_map, 'facilities_docs',
                                         label_col='FACNAME', secondary_label_col='document',
                                         layer_type='marker', filter_on='document', color='black')

    wells = map_dict['wells']
    well_layer = create_layer(wells, 'wells with docs',
                              label_col='wlbWell', secondary_label_col='document',
                              layer_type='marker', filter_on='document', color='red')
    well_layer_no_docs = create_layer(wells, 'wells with docs',
                                      label_col='wlbWell', secondary_label_col='document',
                                      layer_type='marker', filter_on='document', inverse=True, color='lightGray')

    marker_cluster = MarkerCluster(markers=well_layer.layers, name='Wells with Docs')
    marker_cluster2 = MarkerCluster(markers=well_layer_no_docs.layers, name='Wells without Docs')
    # marker_cluster.add_layer(well_layer)
    m.add_layer(structure_layer_docs)
    m.add_layer(structure_layer)
    m.add_layer(fields_layer_docs)
    m.add_layer(fields_layer)
    m.add_layer(subareas_layer)
    m.add_layer(subareas_layer_docs)
    m.add_layer(facilities_layer_docs)
    m.add_layer(facilities_layer)
    m.add_layer(discoveries_layer_docs)
    m.add_layer(discoveries_layer)
    m.add_layer(marker_cluster)
    m.add_layer(marker_cluster2)
    m.add_control(LayersControl())
    m.add_control(FullScreenControl())
    comments = []

    for i in check_cols:
        comments.append(create_layer(final_dataframe[final_dataframe[i] != "Empty"],
                                     i, label_col='wlbWellbor', secondary_label_col=i, layer_type='marker',
                                     color='green'))

        m.add_layer(comments[-1])
    m