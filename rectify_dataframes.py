#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from data_load_functions import create_npd_shapefile_dict

from normalize_csvs import get_dataframes

## take the comments from what i've built and use a column name "csv_name"+comment

dict_dataframes = get_dataframes()

lala = create_npd_shapefile_dict()
