from data_load_functions import *
import pickle as pkl

if __name__ == '__main__':
    key_words = get_key_words()
    data = create_npd_shapefile_dict()
    with open('npd_lookup_dfs.pkl', 'wb') as f:
        pkl.dump(data, f)
    print('here')