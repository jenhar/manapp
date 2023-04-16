import pandas as pd
import numpy as np

def customer_order(d4):
    if len(d4)>0:
        d4=d4.sort_values(by=['spatial_score','mandiri_score'],
                        ascending = [False, True]).head(200).reset_index(drop=True)
        d4['no_idx']=d4.index+1
        kams=dict(zip(d4['no'],d4['no_idx']))
        d4['no']=d4.index+1
        d4=d4.drop(columns=['no_idx'])
        
        return d4, kams
    else:
        return np.NaN, np.NaN

def noncustomer_order(d4):

    if len(d4)>0:

        d4=d4.sort_values(by=['spatial_score'],
                        ascending = [False]).head(200).reset_index(drop=True)
        d4['no_idx']=d4.index+1
        
        kams=dict(zip(d4['no'],d4['no_idx']))
        
        d4['no']=d4.index+1
        
        d4=d4.drop(columns=['no_idx'])
        
        return d4, kams
    else:
        return np.NaN, np.NaN
    
    
def undifind_order(d4):
    if len(d4)>0:

        d4=d4.sort_values(by=['mandiri_score'],
                        ascending = [True]).head(200).reset_index(drop=True)
        d4['no_idx']=d4.index+1
        
        kams=dict(zip(d4['no'],d4['no_idx']))
        
        d4['no']=d4.index+1
        
        d4=d4.drop(columns=['no_idx'])
        
        return d4, kams
    else:
        return np.NaN, np.NaN


def allcustomer_order(d3):

    if len(d3)>0:

        d4=d3.copy()
        d4['no_idx']=d4.index+1
        
        kams=dict(zip(d4['no'],d4['no_idx']))
        
        del d4
        
        return kams
    else:
        kams={'None':'None'}
        return kams
    