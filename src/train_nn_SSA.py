#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May  7 09:16:31 2026

@author: Alberto Zoccante
Data preparation for SSA prediction
"""

#%% Basic imports
from os import getcwd
from os.path import isfile, isdir
from copy import deepcopy
from pprint import pprint
from datetime import datetime
import numpy as np
from inference import run_inference_SSA
from surface import compute_SSA
import pandas as pd
import pathlib
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d
from glob import glob

#%%
def read_ssa(a_SSA_file):
    o_ssas = []
    with open(a_SSA_file) as ssa_f:
        for line in ssa_f.readlines():
            if line[0]=="#":
                continue
            elif len(line.split()) == 2:
                o_ssas.append(float(line.split()[1]))
    return np.array(o_ssas)
                
#%% Script entrypoint.
import argparse

gTest = False

if __name__ == "__main__" and not gTest:

    parser = argparse.ArgumentParser(description=''' Use a machine learning model trained on the carbon model dataset to estimate the porous volume distribution (PVD)
and predict the H2 adsorption isotherm from a N2 adsorption isotherm
Require as argument the name of the system (e.g. maxsorb_H2)
Expect in the same directory the N2 isotherm file: f"{name}_N2_isotherm.txt" 
(which should also contain the total porous volume)
''')
    parser.add_argument('-isotherms', metavar='isotherms_path',help='Isotherm files path.')
    parser.add_argument('-features', metavar='features_path',help='VminD files path.')
    parser.add_argument('-SSA', metavar='SSAs_path',help='SSA file path.')

    parser.add_argument('--output',help='Output files prefix.',default="")

    args = parser.parse_args()
    print(f'features str is {getcwd()+ "/"+ args.features + "/*_VMinD.txt"}')
    feature_files = glob(getcwd()+ "/"+ args.features + "/*_VMinD.txt")
    print(f'isotherms str is {getcwd()+ "/"+ args.isotherms + "/*.isotherm"}')
    isotherms_fs = glob(getcwd()+ "/"+ args.isotherms + "/*.isotherm" )
    SSA = args.SSA
    output = args.output
    if len(output) > 0:
        output = output + "_"

    #: get isotherm data. Assuming (for now) the experimental file has already been processed to get the interpolated adsorption at the fixed N2 pressures.
    n_headers_rows = 0
    models = []
    isotherms = []
    tot_vols = []
    fact = 0.5
    if len(isotherms_fs) == 0:
        exit('Please provide at least an adsorption isotherm of the system on which to train the NN.')
    else:
        for isotherm in isotherms_fs:
            
            if not isfile(isotherm):
                exit(f"File {isotherm} not found.")    
            
            models.append(isotherm.split("/")[-1].replace("_N2.isotherm",""))
            isotherms.append(np.loadtxt(isotherm,skiprows=n_headers_rows)[:,6])
            tot_vols.append((fact*isotherms[-1][-1]+(1-fact)*isotherms[-1][-2])*28/0.807) #volume in CC per sample. Adjusted to improve NN predictivity.
            # print(tot_vols[-1])

        
            

    isotherms = np.array(isotherms)
    print(isotherms.shape)
    
    VMinDs = []
    #Now reading VminDs
    if len(feature_files) == 0:
        exit('Please provide a VMinD profile of the system to analyze.')
    else:
        for feat_f in feature_files:
            
            if not isfile(feat_f):
                exit(f"File {feat_f} not found.")    
            
            VMinDs.append(np.loadtxt(feat_f,skiprows=n_headers_rows)[:,1])
        
    VMinDs  = np.array(VMinDs) 
    print(VMinDs.shape)

    #Now reading SSAs
    if len(SSA) == 0:
        exit('Please provide a SSA list of the systems to analyze.')
    else:
       if not isfile(SSA):
           exit(f"File {SSA} not found.")    
       
       SSAs = read_ssa(SSA)
       
       print(SSAs.shape)
    
    #preparation of df for inference.py
    input_dict= {}

    for i_m,model in enumerate(models):
        if "Sample" not in input_dict.keys():
            input_dict["Sample"]=[model]
        else:   
            input_dict["Sample"].append(model)
            
        for iv,v_minD in enumerate(VMinDs[i_m,:]):
            if f"feature{iv+1}" not in input_dict.keys():
                input_dict[f"feature{iv+1}"] = [v_minD]
            else:
                input_dict[f"feature{iv+1}"].append(v_minD)
                
        for ip,ads in enumerate(isotherms[i_m,:]):
            if f"adsor{ip+1}" not in input_dict.keys():
                input_dict[f"adsor{ip+1}"] = [ads]
            else:
                input_dict[f"adsor{ip+1}"].append(ads)
            
        if "Total volume" not in input_dict.keys():
            input_dict["Total volume"]=[tot_vols[i_m]]
        else:
            input_dict["Total volume"].append(tot_vols[i_m])
        
    input_df = pd.DataFrame.from_dict(input_dict)
    input_df.to_csv("input.dat",sep=",",index=False)
    
    output_dict= {"Sample" :  []}

    for i_m,model in enumerate(models):
        output_dict["Sample"].append(model)
        for iv,v_minD in enumerate(VMinDs[i_m,:]):
            if f"feature{iv+1}" not in output_dict.keys():
                output_dict[f"feature{iv+1}"] = [v_minD]
            else:
                output_dict[f"feature{iv+1}"].append(v_minD)
                
        if "SSA" not in output_dict.keys():
            output_dict["SSA"]=[tot_vols[i_m]]
        else:
            output_dict["SSA"].append(tot_vols[i_m])
                
    output_df = pd.DataFrame.from_dict(output_dict)
    output_df.to_csv("output.dat",sep=",",index=False)
    
        

    

