#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May  7 09:16:31 2026

@author: Alberto Zoccante
Data preparation for adsorption prediction
"""

#%% Basic imports
from os import getcwd
from os.path import isfile, isdir
from copy import deepcopy
from pprint import pprint
from datetime import datetime
import numpy as np
from inference import run_inference
import pandas as pd
import pathlib
import matplotlib.pyplot as plt
#%% Script entrypoint.
import argparse

gTest = False

if __name__ == "__main__" and not gTest:

    parser = argparse.ArgumentParser(description=''' Use a Neural Network trained on the carbon model dataset to estimate the porous volume distribution (PVD)
and predict the H2 adsorption isotherm from a N2 adsorption isotherm
Require as argument the name of the system (e.g. maxsorb_H2)
Expect in the same directory the N2 isotherm file: f"{name}_N2_isotherm.txt" 
(which should also contain the total porous volume)
''')
    parser.add_argument('-isotherm', metavar='isotherm_path',help='Isotherm file path.')
    parser.add_argument('--format',help='Isotherm format: excess adsorption data as mol/g or CC(STP)/g. Available options are "mol" (for mol/g) and "cc" (for CC(STP)/g).',default="mol")
    parser.add_argument('--output',help='Output files prefix.',default="")
    parser.add_argument('--method',help='regressor method',default="regular")
    # parser.add_argument('--tot_vol',help='Total volume',default=1.42)

    args = parser.parse_args()
    isotherm_f = args.isotherm
    # tot_vol = float(args.tot_vol)
    output = args.output
    if len(output) > 0:
        output = output + "_"

    if isotherm_f == "":
        exit('Please provide an adsorption isotherm of the system to analyze.')
    else:
        isotherm = getcwd()+f"/{isotherm_f}"
        if not isfile(isotherm):
            exit(f"File {isotherm} not found.")
    
    if args.method != "neuralregressor" and args.method in ["with_exp", "cut", "partial"]:
        method = "neuralregressor_" + args.method 
    elif args.method == "regular":
        method = "neuralregressor"
    else:
        exit("Neural regressor method not recognized.")
    
    N2_pressures = [ 0.112000E-04,  0.149000E-04,  0.200000E-04,  0.268000E-04,  0.359000E-04,  0.481000E-04,  0.645000E-04,  0.864000E-04,  0.115740E-03,  0.155050E-03,  0.207710E-03,  0.278260E-03,  0.372760E-03,  0.499360E-03,  0.668960E-03,  0.896150E-03,  0.120050E-02,  0.160820E-02,  0.215440E-02,  0.288610E-02,  0.386640E-02,  0.517950E-02,  0.693860E-02,  0.929510E-02,  0.124520E-01,  0.166810E-01,  0.223460E-01,  0.299360E-01,  0.401030E-01,  0.537230E-01,  0.719690E-01,  0.964110E-01,  0.129150E+00,  0.173020E+00,  0.231780E+00,  0.310500E+00,  0.415960E+00,  0.557230E+00,  0.746480E+00,  0.100000E+01 ]
    H2_pressures = [0.01,  0.02,  0.05,  0.10,  0.20,  0.45,  0.91,  1.36,  1.81,  2.27,  2.73,  3.18,  3.63,  4.09,  4.54,  5.00,  6.50,  8.00,  9.50,  11.00,  12.50,  14.00,  15.50,  17.00,  18.50,  20.00,  31.11,  42.22,  53.33,  64.44,  75.56,  86.67,  97.78,  108.89,  120.00]
    
        
    #: get isotherm data. Assuming (for now) the experimental file has already been processed to get the interpolated adsorption at the fixed N2 pressures.
    n_headers_rows = 0
    isotherm_data_orig = np.loadtxt(isotherm,skiprows=n_headers_rows)
    if len(N2_pressures) != isotherm_data_orig.shape[0]:
        ads = np.interp(N2_pressures,isotherm_data_orig[:,0],isotherm_data_orig[:,])
        isotherm_data = np.column_stack((np.array(N2_pressures),ads))
    else:
        isotherm_data = isotherm_data_orig
        
    #Computing total volume
    fact = 0.5

    if args.format == "mol":
    
        tot_vol = (fact*isotherm_data[-1,1]+(1-fact)*isotherm_data[-2,1])*28/0.808 #volume in CC per sample. Adjusted to improve NN predictivity.
    elif args.format == "cc":
        tot_vol = (fact*isotherm_data[-1,1]+(1-fact)*isotherm_data[-2,1])*0.001545 #volume in CC per sample. Adjusted to improve NN predictivity.

    #preparation of df for inference.py
    input_dict= {"Sample" :  "Test"}
    for ip,ads in enumerate(isotherm_data[:,1]):
        if args.format == "cc": #converting between CC(STP)/g to mol/g
            ads = ads/22414 # mol/g
        input_dict[f"adsor{ip}"] = [ads]
    input_dict["Total volume"] = [tot_vol]
        
    input_df = pd.DataFrame.from_dict(input_dict)
    input_df.to_csv("input.dat",sep="\t")
    
    
    out_d = getcwd()+"/predictions/" #Expecting these dirs to be in the same dir as the script.
    scrpath = pathlib.Path(__file__).parent.resolve()
    
    model_path = scrpath / pathlib.Path(f"{method}")
    
    #running inference
    idx,Ypred,Zpred = run_inference(input_df, out_d , model_path) 
    
    #Plotting VminD
    
    plt.title("VminD")
    plt.bar(range(1,61,1),Zpred[0,:])
    plt.xlabel(r"$\AA$")
    plt.ylabel(r"$cm^3/g$")
    plt.savefig(getcwd()+f"/predictions/{output}VminD.png",dpi=300)
    plt.show()
    
    #Plotting simplified VminD
    
    u=0
    m=0
    sm=0
    lm=0
    mc=0
    for b,h in zip(range(1,61,1),Zpred[0,:]):
        if b <= 7.0:
            u += h
        elif (b > 7.0) and (b <= 20.0):
            m+=h
        elif (b > 20.0) and ( b <= 35.0):
            sm += h
        elif (b > 35.0) and (b <= 50.0):
            lm += h 
        elif (b > 50.0):
            mc += h
        else:
            print("WARNING: Negative minD found. Something went wrong. Check your data.")
            
    tot=u+m+sm+lm+mc
    sVminD = [tot,u,m,sm,lm,mc]
    labels = ["Total",r"< 7 $\AA$",r"7$\AA$-20$\AA$",r"20$\AA$-35$\AA$",r"35$\AA$-50$\AA$",r">50$\AA$"]
    bar_colors = ['lightgray', 'red', 'mediumblue', 'greenyellow','mediumslateblue']
    
    fig,ax = plt.subplots()
    ax.set_title("Simplified VminD")

    ax.bar(range(1,7),sVminD,color=bar_colors)
    ax.set_xlabel(r"MinD $\AA$")
    ax.set_ylabel(r"Porous volume $cm^3/g$")
    ax.set_xticks(range(1,7), labels)
    plt.savefig(getcwd()+f"/predictions/{output}VminD_simplified.png",dpi=300)
    plt.show()
    
    
    #Plotting Cumulative VMinD
    
    cumulative_VMinD = np.cumsum(Zpred)
    
    plt.title("Cumulative VminD")

    plt.plot(range(1,61,1),cumulative_VMinD,marker='s', markersize=3, linestyle='-', linewidth = 0.5)
    plt.xlabel(r"$\AA$")
    plt.ylabel(r"$cm^3/g$")
    plt.savefig(getcwd()+f"/predictions/{output}VminD_cumulative.png",dpi=300)
    plt.show()
    
    
    #Plotting H2 isotherm
    plt.title(r"$H_2$ excess adsorption @77K")

    plt.plot(H2_pressures,Ypred[0,:]*1000,marker='.', markersize=4, linestyle='-', linewidth = 0.5)
    plt.xlabel("P (bar)")
    plt.ylabel("Excess ads. (mol/kg)")
    plt.savefig(getcwd()+f"/predictions/{output}predicted_H2_isotherm_77K.png",dpi=300)
    plt.show()
    



