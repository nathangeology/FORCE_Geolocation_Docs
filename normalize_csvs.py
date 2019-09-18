#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import pandas as pd

def get_datafames():
    folder = "/home/dimitrisl/Desktop/FORCE_Geolocation_Docs/sample_data/Norwegian well  completion reports and label data for hydrocarbon shows"
    keep_csvs = { i: folder+"/"+i for i in os.listdir(folder) if ".csv" in i}
    print("found", keep_csvs.keys()) 
    csv_dataframes = {i: pd.read_csv(keep_csvs[i], sep=';', skiprows=range(9), encoding='iso-8859-1') for i in keep_csvs.keys() }
    return csv_dataframes