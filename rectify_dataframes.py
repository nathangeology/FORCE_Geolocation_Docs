#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from data_load_functions import create_npd_shapefile_dict
import numpy as np
import pandas as pd
from normalize_csvs import get_dataframes

## take the comments from what i've built and use a column name "csv_name"+comment

dict_dataframes = get_dataframes()

original_npd_dataframes = create_npd_shapefile_dict()

collumns_to_be_added = [ i.split(".")[0]+" comment" for i in dict_dataframes.keys()]

npd_dataframes = pd.DataFrame(original_npd_dataframes["well_bores"].copy())

for i in collumns_to_be_added:
    npd_dataframes[i] = "Empty"

print(npd_dataframes[npd_dataframes["wlbWellbor"]=="6607/5-1"])

#['flour.csv', 'odor.csv', 'streaming.csv', 'good show.csv', 
#'flourescense.csv', 'stain.csv', 'no shows.csv', 'fluor.csv', 'odour.csv']

# it seems that the naming pattern followed by the "well_bores" dataframe
# is  XXX/YYY-ZZZ
# so instead we will convert our current wells to follow that pattern

for csv in dict_dataframes:
    w_n = dict_dataframes[csv].columns[0]
    dict_dataframes[csv][w_n] = dict_dataframes[csv][w_n].apply(lambda x: x.replace("_","/", 1))

    npd_wl = set(npd_dataframes["wlbWellbor"])
    for well in dict_dataframes[csv][w_n]:

        c_a = csv.split(".")[0] + " comment"
        if well in npd_wl:
            last_valid = (well, c_a)
            npd_dataframes.loc[npd_dataframes["wlbWellbor"]==well, c_a] = str(dict_dataframes[csv][c_a][ dict_dataframes[csv][w_n] == well ])


