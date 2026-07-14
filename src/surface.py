#Sout: estimated ASA from VMinD and PoLA surface/volume 

import os
from os.path import join
import numpy as np
import pathlib
#import pandas as pd

#%%
def read_ratios():
    scrpath = pathlib.Path(__file__).parent.resolve()
    ratios = np.loadtxt(join(scrpath,"S_V_ratios.dat"),delimiter =",")
    return ratios[:,3]

def compute_SSA(aVMinD):
    
    n_len = aVMinD.shape[0]
    ratios = read_ratios()
    
    surf_layer_vol = np.dot(ratios[:n_len],aVMinD)
    
    N2_density=0.808
    N2_cross_section=16.2
    N2_molec_weight=28
    Avogadro=6.022E+23
    A2_to_m2=1.0E-20
    
    Molec_Layer = surf_layer_vol * N2_density * Avogadro / N2_molec_weight
    SSA = Molec_Layer * N2_cross_section * A2_to_m2
    
    return SSA