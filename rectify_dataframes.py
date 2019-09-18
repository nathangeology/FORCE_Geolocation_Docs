#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from data_load_functions import create_npd_shapefile_dict
import numpy as np
from normalize_csvs import get_dataframes

## take the comments from what i've built and use a column name "csv_name"+comment

dict_dataframes = get_dataframes()

npd_dataframes = create_npd_shapefile_dict()

collumns_to_be_added = [ i.split(".")[0]+" comment" for i in dict_dataframes.keys()]

for i in collumns_to_be_added:
    npd_dataframes["well_bores"][i] = np.nan

#['flour.csv', 'odor.csv', 'streaming.csv', 'good show.csv', 
#'flourescense.csv', 'stain.csv', 'no shows.csv', 'fluor.csv', 'odour.csv']

# it seems that the naming pattern followed by the "well_bores" dataframe
# is  XXX/YYY-ZZZ
# so instead we will convert our current wells to follow that pattern

for csv in dict_dataframes:
    w_n = dict_dataframes[csv].columns[0]
    dict_dataframes[csv][w_n] = dict_dataframes[csv][w_n].apply(lambda x: x.replace("_","/", 1))

    npd_wl = set(npd_dataframes["well_bores"]["wlbWellbor"])    
    
    for well in dict_dataframes[csv][w_n]:
        c_a = csv.split(".")[0] + " comment"
        if well in npd_wl:
# geo pandas are not hashable. which means i cannot use the next line            
            npd_dataframes[npd_dataframes["well_bores"] == well][c_a] = dict_dataframes[csv][c_a][ dict_dataframes[csv][w_n] == well ]
# converted every well name


