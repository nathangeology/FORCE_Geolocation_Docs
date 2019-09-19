import geopandas as gpd
import pandas as pd
import numpy as np
from data_load_functions import *
import pickle

if __name__ == '__main__':
    objects = []
    with open('joined_dfs.pkl', 'rb') as openfile:
        while True:
            try:
                objects.append(pkl.load(openfile))
            except EOFError:
                break
    mudlog_well_header = objects[0]
    get_keywords_doc = pd.read_csv('result.csv')
    get_keywords_doc['cleaned_doc'] = get_keywords_doc['document'].apply(clean_doc_name)
    get_keywords_doc.set_index(['keyword', 'cleaned_doc'],
                               inplace=True,
                               drop=False)
    doc_keywords_set = set(get_keywords_doc['keyword'])
    shape_files_dict = create_npd_shapefile_dict()
    key_cols = get_key_cols()
    for key, value in shape_files_dict.items():
        if key == 'well_header':
            continue
        keyword_col = key_cols[key]
        value['cleaned_keywords'] = value[keyword_col].apply(clean_text)
        shape_keyset = set(value['cleaned_keywords'])
        matched_keys = shape_keyset.intersection(doc_keywords_set)
        for matched_key in list(matched_keys):
            print('here')
        print('here')