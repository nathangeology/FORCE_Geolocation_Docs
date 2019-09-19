from ipyleaflet import LayerGroup, Popup, Polygon, Marker
from ipywidgets import HTML
import geopandas as gpd
import pandas as pd


def clean_table(geo_table):
    filter_list = []
    append_tables = []
    current_crs = geo_table.crs
    for idx, row in geo_table.iterrows():
        if row['geometry'] is None:
            filter_list.append(False)
        elif str(type(row['geometry'])) == '<class \'shapely.geometry.multipolygon.MultiPolygon\'>':
            filter_list.append(False)
            exploded_polygons = row.explode()['geometry']
            gpd.GeoDataFrame(geometry=exploded_polygons)
            temp_table = gpd.GeoDataFrame(geometry=exploded_polygons)
            for key, item in row.items():
                if key != 'geometry':
                    temp_table[key] = item
            append_tables.append(temp_table)
        else:
            filter_list.append(True)
    geo_table = geo_table[filter_list]
    append_tables.append(geo_table)
    geo_table = gpd.GeoDataFrame(pd.concat(append_tables, ignore_index=True))
    geo_table.crs = current_crs
    geo_table = geo_table.to_crs(epsg=4326)
    return geo_table


def create_layer(geo_table, name, label_col=None, layer_type=None):
    output = LayerGroup(name=name)
    geo_table = clean_table(geo_table)
    if layer_type is None:
        raise(ValueError('must provide a type of layer to make with table!'))
    for _, row in geo_table.iterrows():
        if layer_type == 'polygon':
            y = list(row.geometry.exterior.coords.xy[1])
            x = list(row.geometry.exterior.coords.xy[0])
            locations = [(y, x) for y, x in zip(y, x)]
            temp_layer = Polygon(locations=locations,
                color="orange",
                fill_color="orange",
            )
        elif layer_type == 'marker':
            temp_layer = Marker(location=(row.geometry.y, row.geometry.x))
        if label_col is not None:
            message = HTML()
            message.value = row[label_col]
            temp_layer.popup = message
        output.add_layer(temp_layer)
    return output
