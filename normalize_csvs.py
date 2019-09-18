#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import pandas as pd


def compare_well_names(well1, well2, s_chars=["/","-"," "]):
    
    for x,y in zip(well1,well2):
        if x!=y:
            if (x in s_chars) and (y in s_chars):
                continue
            else:
                print(well1,"!=",well2)
                return False
    
    return True


def name_cleaner(word):
    
    intermediate = ["COMPLETION_REPORT", "WELL", "PB", "AND"]
    
    for i in intermediate:
        if i in word:
            sp = i
            word = word.split(sp)[0]
    while True :
        if not (word[-1].isalpha() or word[-1].isdigit()) :
            word = word[:-1]
        else:
            break
    return word


def get_dataframes():
    folder = "sample_data/Norwegian well  completion reports and label data for hydrocarbon shows"
    keep_csvs = { i: folder+"/"+i for i in os.listdir(folder) if ".csv" in i}
    print("found", keep_csvs.keys()) 
    
    csv_dataframes = {}
    for i in keep_csvs.keys():
        csv_dataframes[i] = pd.read_csv(keep_csvs[i], sep=';', skiprows=range(9), encoding='iso-8859-1')
        temp_clean = csv_dataframes[i]
        col = temp_clean.columns[-1]
        csv_dataframes[i] = temp_clean[temp_clean[col] != col].copy()
        csv_dataframes[i].rename(columns={ col: i.split(".")[0]+" comment"}, 
                 inplace=True)
        
        names_col = temp_clean.columns[0]
        csv_dataframes[i][names_col] = csv_dataframes[i][names_col].apply(name_cleaner)
        
        csv_dataframes[i] = csv_dataframes[i].groupby(names_col, as_index=False).agg(lambda x :','.join(x))

        
        temp_clean = None
        
    return csv_dataframes


#get_dataframes()