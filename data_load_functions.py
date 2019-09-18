try:
    import geopandas as gpd
except Exception as ex:
    print(ex)
import pandas as pd
import pickle as pkl

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

def string_cleaner(a_string:str):
    output = a_string
    output = output.replace('\u00C5', 'aa')
    output = output.replace('\u00E5', 'aa')
    output = output.replace('\u00C6', 'ae')
    output = output.replace('\u00E6', 'ae')
    output = output.replace('\u00C8', 'oe')
    output = output.replace('\u00E8', 'oe')
    output = output.lower()

    return output

def get_key_words():
    key_cols = {
        'blocks': 'LABEL',
        'discoveries': 'DISCNAME',
        'well_bores': 'wlbWellbor',
        'wells': 'wlbWell',
        'facilities': 'FACNAME',
        'fields': 'FIELDNAME',
        'structures': 'steNameNO',
        'structures_en': 'steNameEN',
        'basins': 'steTopogra',
        'sub_areas': 'NAME',
    }
    output = []
    type = []
    try:
        data_dict = create_npd_shapefile_dict()
    except Exception as ex:
        object = []
        with open('npd_lookup_dfs_no_geopandas.pkl', 'rb') as openfile:
            while True:
                try:
                    object.append(pkl.load(openfile))
                except EOFError:
                    break
        data_dict = object[0]
    for key, value in data_dict.items():
        if 'well_header' not in key:
            df = pd.DataFrame(value)
            temp = list(df[key_cols[key]])
            temp = [string_cleaner(x) for x in temp]
            temp_type = [key] * len(temp)
            type += temp_type
            output += temp
    return output, type

def strip_out_geopandas(data_dict):
    output = {}
    for key, value in data_dict.items():
        if 'well_header' not in key:
            df = pd.DataFrame(value)
            output[key] = df
        else:
            output[key] = value
    return output

