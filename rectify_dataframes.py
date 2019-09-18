#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from data_load_functions import create_npd_shapefile_dict

from normalize_csvs import get_dataframes

## take the comments from what i've built and use a column name "csv_name"+comment


def name_cleaner(word):
    intermediate = ["_COMPLETION_REPORT_", "__WELL__", "_PB"]
    if intermediate[0] in word:
        sp = intermediate[0]
    elif intermediate[1] in word:
        sp = intermediate[1]
    elif intermediate[2] in word:
        sp = intermediate[2]
    else:
        return word
    return word.split(sp)[0]




dict_dataframes = get_dataframes()

lala = create_npd_shapefile_dict()
