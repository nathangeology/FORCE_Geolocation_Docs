import geopandas as gpd
import pandas as pd

def load_shape_file(file):
    output = gpd.read_file(file)
    return output

def create_npd_shapefile_dict():
    files = {
        'blocks': 'sample_data/shapefiles/loc_npd_blocks.shp',
        'discoveries': 'sample_data/shapefiles/loc_npd_discoveries.shp',
        'well_bores': 'sample_data/shapefiles/loc_npd_ea_wells.shp',
        'wells': 'sample_data/shapefiles/loc_npd_ea_wells.shp',
        'facilities': 'sample_data/shapefiles/loc_npd_facilities.shp',
        'fields': 'sample_data/shapefiles/loc_npd_fields.shp',
        # 'licenses': 'sample_data/shapefiles/loc_npd_licenses.shp',
        'structures': 'sample_data/shapefiles/loc_npd_struct_elements.shp',
        'structures_en': 'sample_data/shapefiles/loc_npd_struct_elements.shp',
        'basins':  'sample_data/shapefiles/loc_npd_struct_elements.shp',
        'sub_areas': 'sample_data/shapefiles/loc_npd_subareas.shp',
    }
    output = {}
    for key, value in files.items():
        output[key] = load_shape_file(value)
    output['well_header'] = pd.read_csv('sample_data/with-coordinates.csv', delimiter=';')
    return output


def get_key_words():
    key_cols = {
        'blocks': 'LABEL',
        'discoveries': 'Shape_Leng',
        'wells': 'wlbWellbor',
        'well_bores': 'wlbWell',
        'facilities': 'FACNAME',
        'fields': 'FIELDNAME',
        'structures': 'steNameNO',
        'structures_en': 'steNameEN',
        'basins': 'steTopogra',
        'sub_areas': 'NAME',
    }
    output = []
    type = []
    data_dict = create_npd_shapefile_dict()
    for key, value in data_dict.items():
        if 'well_header' not in key:
            df = pd.DataFrame(value)
            temp = list(df[key_cols[key]])
            temp_type = [key] * len(temp)
            type += temp_type
            output += temp
            print('here')
    return output, type
