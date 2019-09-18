#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import pandas as pd

def get_dataframes():
    folder = "sample_data/Norwegian well  completion reports and label data for hydrocarbon shows"
    keep_csvs = { i: folder+"/"+i for i in os.listdir(folder) if ".csv" in i}
    print("found", keep_csvs.keys()) 
    # csv_dataframes = {i: pd.read_csv(keep_csvs[i], sep=';', skiprows=range(9), encoding='iso-8859-1') for i in keep_csvs.keys() }
    
    csv_dataframes = {}
    for i in keep_csvs.keys():
        csv_dataframes[i] = pd.read_csv(keep_csvs[i], sep=';', skiprows=range(9), encoding='iso-8859-1')
        temp_clean = csv_dataframes[i]
        col = temp_clean.columns[0]
        csv_dataframes[i] = temp_clean[temp_clean[col] != col].copy()
        temp_clean = None
        
    return csv_dataframes
