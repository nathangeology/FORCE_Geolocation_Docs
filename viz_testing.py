import altair as alt
from data_load_functions import *
import folium
import geopandas as gpd
from folium.plugins import MarkerCluster

if __name__ == '__main__':
    map_dict = create_npd_shapefile_dict()
    structures_map = map_dict['structures']
    print(structures_map.crs)
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
    # map_dict['wells'].to_file("wells.geojson", driver='GeoJSON')
    m = folium.Map(location=[60.5236, 0])
    folium.GeoJson(
        'structures.geojson',
        name='structures'
    ).add_to(m)
    wells_df = map_dict['wells']
    wells_df = wells_df.to_crs(epsg=4326)
    wells_df.to_file("wells.geojson", driver='GeoJSON')
    folium.GeoJson(
        'wells.geojson',
        name='wells'
    ).add_to(m)
    # wells = alt.Chart(map_dict['wells']).mark_geoshape(
    #     fill='black',
    #     stroke='black',
    # ).properties(
    #     width=500,
    #     height=500
    # )
    #
    # wells.serve()