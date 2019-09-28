from data_load_functions import *
import pickle as pkl

if __name__ == '__main__':
    key_words = get_key_words()
    data = create_npd_shapefile_dict()
    no_geopandas = strip_out_geopandas(data)
    with open('npd_lookup_dfs_no_geopandas.pkl', 'wb') as f:
        pkl.dump(no_geopandas, f)
    with open('npd_lookup_dfs.pkl', 'wb') as f:
        pkl.dump(data, f)
    print('here')