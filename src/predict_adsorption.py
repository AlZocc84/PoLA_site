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
from surface import compute_SSA
import pandas as pd
import pathlib
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d
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
    parser.add_argument('-isotherm', metavar='isotherm_path',help='Isotherm file path.')
    parser.add_argument('--format',help='Isotherm format: excess adsorption data as mol/g or CC(STP)/g. Available options are "mol" (for mol/g) and "cc" (for CC(STP)/g).',default="mol")
    parser.add_argument('--output',help='Output files prefix.',default="")
    parser.add_argument('--method',help='regressor method',default="regular")
    parser.add_argument('--hide',help='Does not show graphs',action='store_true')
    parser.add_argument('--tot_vol',help='Total volume',default=False)

    args = parser.parse_args()
    isotherm_f = args.isotherm
    tot_vol = float(args.tot_vol)
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
    approx = interp1d(isotherm_data_orig[:,0],isotherm_data_orig[:,1])
    ads  = approx(N2_pressures)

    isotherm_data = np.column_stack((np.array(N2_pressures),ads))
   
        
    print(isotherm_data.shape)
    #Computing total volume
    fact = 0.5

    if not args.tot_vol:
        if args.format == "mol":
            tot_vol = (fact*isotherm_data[-1,1]+(1-fact)*isotherm_data[-2,1])*28/0.807 #volume in CC per sample. Adjusted to improve NN predictivity.
        elif args.format == "cc":
            tot_vol = (fact*isotherm_data[-1,1]+(1-fact)*isotherm_data[-2,1])*0.001545 #volume in CC per sample. Adjusted to improve NN predictivity.

    print(tot_vol)
    #preparation of df for inference.py
    input_dict= {"Sample" :  "Test"}
    for ip,ads in enumerate(isotherm_data[:,1]):
        if args.format == "cc": #converting between CC(STP)/g to mol/g
            ads = ads/22400 # mol/g
        input_dict[f"adsor{ip}"] = [ads]
    input_dict["Total volume"] = [tot_vol]
        
    input_df = pd.DataFrame.from_dict(input_dict)
    input_df.to_csv("input.dat",sep="\t")
    
    
    out_d = getcwd()+"/predictions/" #Expecting these dirs to be in the same dir as the script.
    scrpath = pathlib.Path(__file__).parent.resolve()
    
    model_path = scrpath / pathlib.Path(f"{method}")
    
    #---------------------------------------------------------------------------------------------#
    #running inference
    idx,Ypred,Zpred = run_inference(input_df, out_d , model_path) 
    #---------------------------------------------------------------------------------------------#
    
    ssa = compute_SSA(Zpred[0,:])
    with open(out_d+f"{output}SSA.dat","w") as out_SSA:
        out_SSA.write(f"The SSA is {ssa:6.2f} m^2/g\n")
    #Now outputting results.
    
    #Plotting VminD
    
    plt.title("VminD")
    plt.bar(range(1,61,1),Zpred[0,:])
    plt.xlabel(r"$Å$")
    plt.ylabel(r"$\mathrm{cm}^3/\mathrm{g}$")
    plt.savefig(getcwd()+f"/predictions/{output}VminD.png",dpi=300)
    
    if not args.hide:
        plt.show()
    
    #Writing VMinD data to file
    with open(out_d+f"{output}VminD.dat","w") as out_VMinD:
        out_VMinD.write("# MinD(Å)\tV(MinD)(cm^3/gÅ)\n")
        for d,Vd in zip(range(1,61,1),Zpred[0,:]):
            out_VMinD.write(f"{d}\t{Vd:3.4f}\n")
    
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
    labels = ["Total",r"< 7 $\mathrm{Å}$",r"7$\mathrm{Å}$-20$\mathrm{Å}$",r"20$\mathrm{Å}$-35$\mathrm{Å}$",r"35$\mathrm{Å}$-50$\mathrm{Å}$",r">50$\mathrm{Å}$"]
    bar_colors = ['lightgray', 'red', 'mediumblue', 'greenyellow','mediumslateblue']
    
    fig,ax = plt.subplots()
    ax.set_title("Simplified VminD")

    ax.bar(range(1,7),sVminD,color=bar_colors)
    ax.set_xlabel(r"MinD $\mathrm{Å}$")
    ax.set_ylabel(r"Porous volume $\mathrm{cm}^3/\mathrm{g}$")
    ax.set_xticks(range(1,7), labels)
    plt.savefig(getcwd()+f"/predictions/{output}VminD_simplified.png",dpi=300)
    if not args.hide:
        plt.show()
    
    #Writing simplified VMinD data to file
    f_labels = ["Total",r"< 7 Å",r"7Å-20Å",r"20Å-35Å",r"35Å-50Å",r">50Å"]
    with open(out_d+f"{output}VminD_simplified.dat","w") as out_sVMinD:
        out_sVMinD.write("# Category\tV(MinD)(cm3/g)\n")
        for cat,Vd in zip(f_labels,sVminD):
            out_sVMinD.write(f"{cat}\t{Vd:4.3f}\n")
    
    
    #Plotting Cumulative VMinD
    
    cumulative_VMinD = np.cumsum(Zpred)
    
    fig,ax = plt.subplots()
    ax.set_title("Cumulative VminD")

    ax.plot(range(1,61,1),cumulative_VMinD,marker='s', markersize=3, linestyle='-', linewidth = 0.5)
    ax.set_xlabel(r"$\mathrm{Å}$")
    ax.set_ylabel(r"$\mathrm{cm}^3/\mathrm{g}$")
    plt.savefig(getcwd()+f"/predictions/{output}VminD_cumulative.png",dpi=300)
    if not args.hide:
        plt.show()
    
    #Writing cumulative VMinD data to file
    with open(out_d+f"{output}VminD_cumulative.dat","w") as out_cVMinD:
        out_cVMinD.write("# MinD(Å)\tcumulative_V(MinD)(cm3/g)\n")
        for d,cVd in zip(range(1,61,1),cumulative_VMinD):
            out_cVMinD.write(f"{d}\t{cVd:4.3f}\n")
    
    #Plotting H2 isotherm
    fig,ax = plt.subplots()
    ax.set_title(r"$\mathrm{H}_2$ excess adsorption @77K")

    ax.plot(H2_pressures,Ypred[0,:]*1000,marker='.', markersize=4, linestyle='-', linewidth = 0.5)
    ax.set_xlabel("P (bar)")
    ax.set_ylabel("Excess ads. (mol/kg)")
    plt.savefig(getcwd()+f"/predictions/{output}predicted_H2_isotherm_77K.png",dpi=300)
    if not args.hide:
        plt.show()
    
    #Writing estimated H2 isotherm data to file
    with open(out_d+f"{output}H2_adsorption_predicted.dat","w") as out_cVMinD:
        out_cVMinD.write("# P(bar)\tExcess_H2_adsorption(mol/kg)\n")
        for p,adsH2 in zip(H2_pressures,Ypred[0,:]*1000):
            out_cVMinD.write(f"{p:.2E}\t{adsH2:4.3f}\n")


