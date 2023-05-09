import numpy as np

def transactioncredit(trx_3mo,trx_6mo,trx_9mo,trx_12mo):
    try:
        a=(trx_6mo/trx_3mo)-1
    except:
        a=0
        
    try:
        b=(trx_9mo/trx_6mo)-1
    except:
        b=0
    
    try:
        c=(trx_12mo/trx_9mo)-1
    except:
        c=0
    
    z=np.mean([a,b,c])
    if z >= 0.1:
        return 1
    else:
        return 0


def transactiondebit(trx_3mo,trx_6mo,trx_9mo,trx_12mo):
    try:
        a=(trx_6mo/trx_3mo)-1
    except:
        a=0
        
    try:
        b=(trx_9mo/trx_6mo)-1
    except:
        b=0
    
    try:
        c=(trx_12mo/trx_9mo)-1
    except:
        c=0
    
    z=np.mean([a,b,c])
    if z >= 0.1:
        return 1
    else:
        return 0
    

def balance(trx_3mo,trx_6mo,trx_9mo,trx_12mo):
    try:
        a=(trx_6mo/trx_3mo)-1
    except:
        a=0
        
    try:
        b=(trx_9mo/trx_6mo)-1
    except:
        b=0
    
    try:
        c=(trx_12mo/trx_9mo)-1
    except:
        c=0
    
    z=np.mean([a,b,c])
    if z >= 0.1:
        return 1
    else:
        return 0
    

def closeloop_rate_tr(x):
    if x >= 0.7:
        return 1
    else:
        return 0
    

def ops_in_other_bank(x):
    if x >=0.5:
        return 1
    else:
        return 0


def online_usingrate(x):
    if x >=0.5:
        return 1
    else:
        return 0
    
    
def balance_casa_to_credit(trx_3mo,trx_6mo,trx_9mo,trx_12mo,avgbal_3mo,agvbal_6mo,agvbal_9mo,agvbal_12mo):
    try:
        a=(avgbal_3mo/trx_3mo)-1
    except:
        a=0
        
    try:
        b=(avgbal_6mo/trx_6mo)-1
    except:
        b=0
    
    try:
        c=(avgbal_9mo/trx_9mo)-1
    except:
        c=0
        
    try:
        d=(avgbal_12mo/trx_12mo)-1
    except:
        d=0
    
    z=np.mean([a,b,c,d])
    if z >= 0.1:
        return 1
    else:
        return 0
    
    

def mandiri_new_parameter(df):
    
    
    df['transaction_credit']=[transactioncredit(x,y,z,z1) for x,y,z,z1 in zip(df['total_trx_kredit_amount_3mo'],
                                                                              df['total_trx_kredit_amount_6mo'],
                                                                              df['total_trx_kredit_amount_9mo'],
                                                                              df['total_trx_kredit_amount_12mo'])]


    df['balance_casa_to_credit']=[balance_casa_to_credit(w,x,y,z,w1,x1,y1,z1) for w,x,y,z,w1,x1,y1,z1 in zip(df['total_trx_kredit_amount_3mo'],
                                                                                                        df['total_trx_kredit_amount_6mo'],
                                                                                                        df['total_trx_kredit_amount_9mo'],
                                                                                                        df['total_trx_kredit_amount_12mo'],
                                                                                                        df['avgbal_casa_3mo'],
                                                                                                        df['avgbal_casa_6mo'],
                                                                                                        df['avgbal_casa_9mo'],
                                                                                                        df['avgbal_casa_12mo'])]

    df['transaction_debit']=[transactiondebit(x,y,z,z1) for x,y,z,z1 in zip(df['total_trx_debit_amount_3mo'],
                                                                              df['total_trx_debit_amount_6mo'],
                                                                              df['total_trx_debit_amount_9mo'],
                                                                              df['total_trx_debit_amount_12mo'])]


    df['balance']=[balance(x,y,z,z1) for x,y,z,z1 in zip(df['avgbal_casa_3mo'],
                                                         df['avgbal_casa_6mo'],
                                                         df['avgbal_casa_9mo'],
                                                         df['avgbal_casa_12mo'])]

    df['closeloop_rate_transaction']=[closeloop_rate_tr(x) for x in df['closeloop_rate']]

    df['other_bank_rate']=[ops_in_other_bank(x) for x in df['operating_in_other_bank_rate']]

    df['online_using_rate_sc']=[online_usingrate(x) for x in df['online_using_rate']]
    



def mandiri_new_socre(df):
    data2=['transaction_credit','balance_casa_to_credit','transaction_debit','balance','closeloop_rate_transaction','other_bank_rate','online_using_rate_sc']
    df['mandiri_score'] = df[data2].sum(axis=1, skipna=True)
    
    

    


