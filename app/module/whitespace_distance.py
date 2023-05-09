from sklearn.preprocessing import MinMaxScaler
import re
from fuzzywuzzy import fuzz
from shapely.geometry import Point
from math import radians, cos, sin, asin, sqrt
import numpy as np
import os
import pandas as pd
import geopandas as gpd
import glob
import pyproj
geod = pyproj.Geod(ellps='WGS84')


def categori_type(n, m, s):
    if m > 0 and n >= 49 and s > 0:
        return 'customer'

    elif m > 0 and s == 0 and n == 0:
        return 'undefined customer'

    elif m > 0 and s > 0 and n < 49:
        return 'undefined customer'

    # elif m > 0 and s > 0 and n == 0:
    #     return 'non customer'

    elif m == 0 and s > 0 and n == 0:
        return 'non customer'


def mandiri_score(df_selection):
    d4 = df_selection.copy()
    data2 = ['product_sc', 'channel_sc', 'online_score']
    dataaa = [25, 25, 50]

    d4['product_sc'] = d4[['is_deposit', 'is_giro','is_tabungan']].sum(
        axis=1, numeric_only=True)
    d4['channel_sc'] = d4[['flag_mcm1', 'flag_mcm2',
                           'flag_mgt', 'flag_mib', 'flag_scm']].sum(axis=1, numeric_only=True)
    d4['online_score'] = d4[['online_using_rate']].sum(
        axis=1, numeric_only=True)

    scaler = MinMaxScaler()
    d4[data2] = scaler.fit_transform(d4[data2])
    rockam = dict(zip(data2, dataaa))

    for i, j in enumerate(data2):
        d4[j] = round(d4[j]*rockam[j], 3)

    df2 = d4.copy()
    df2['mandiri_score'] = df2[data2].sum(axis=1, skipna=True)

    return df2


def spatial_score(df_selection):
    data = df_selection.copy()
    data2 = ['access', 'u15_u55', 'rating', 'reviewers', 'mobile data (avg)']
    dataaa = [20, 20, 20, 20, 20]

    scaler = MinMaxScaler()
    data[data2] = scaler.fit_transform(data[data2])
    rockam = dict(zip(data2, dataaa))

    for i, j in enumerate(data2):
        data[j] = round(data[j]*rockam[j], 3)

    df2 = data.copy()
    df2['spatial_score'] = df2[data2].sum(axis=1, skipna=True)

    return df2


def nlp_value(df11, val1, val2):
    df11['nlp_score'] = [fuzz.token_set_ratio(
        x, y) for x, y in zip(df11[val1], df11[val2])]


def creategeom(a):
    y = float(re.findall(r'[-?\d\.\d]+', a)[0])
    x = float(re.findall(r'[-?\d\.\d]+', a)[1])
    try:
        p = Point(x, y)
    except:
        p = Point(0, 0)

    return p


def setgeom(df1):
    df1 = df1.set_geometry('geom')
    df1.set_crs = 'epsg:4326'
    return df1

    
def setlonlat(df):
    df['lon'] = df.geometry.apply(lambda p: p.x)
    df['lat'] = df.geometry.apply(lambda p: p.y)


# df1['geom']=[creategeom(x) for x in df1['lonlat']]
# df1=setgeom(df1)
# setlonlat(df1)
# nlp_value(df1, 'name', 'poi_name')


def eulcideans_pyproj(x, y, x1, y1):
    a1, a2, d = geod.inv(x, y, x1, y1)
    return d


def haversine(lon1, lat1, lon2, lat2):
    """
    Calculate the great circle distance between two points 
    on the earth (specified in decimal degrees)
    """
    # convert decimal degrees to radians
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    # haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a))
    # Radius of earth in kilometers is 6371
    km = 6371 * c
    return km * 1000


def find_nearest(df, lat, long, nama_colum):
    distances = df.apply(
        lambda row: haversine(lat, long, row['lat'], row['lon']),
        axis=1)
    return df.loc[distances.idxmin(), nama_colum]


def matrix_distance(df, lat, long):
    distances = df.apply(
        lambda row: eulcideans_pyproj(long, lat, row['lon'], row['lat']),
        axis=1)
    return distances


def matrix_distance(df, lat, long):
    distances = df.apply(
        lambda row: haversine(lat, long, row['lat'], row['lon']),
        axis=1)
    return distances


def nearestdistances1(data_mandiri, data_bvt, distance):

    df1 = data_mandiri.copy()
    df2 = data_bvt.copy()

    cates = []
    dos = df2.apply(lambda row: matrix_distance(
        df1, row['lat'], row['lon']), axis=1)

    while True:

        #     df2=df2[~df2.index.isin(idxs)]
        #     dos=dos[~dos.index.isin(idxs)]
        #     dos=dos.drop(columns=cols)

        df2['distance'] = np.nanmin(dos.to_numpy(), axis=1)
        df2['name'] = dos.idxmin(axis=1)

        cate = df2[df2['distance'] < distance].sort_values(
            'distance').drop_duplicates('name')
        col = cate['name'].values.tolist()
        idx = cate.index.values.tolist()

    #     for i in col:
    #         cols.append(i)

    #     for i in idx:
    #         idxs.append(i)

        df2 = df2[~df2.index.isin(idx)]
        dos = dos[~dos.index.isin(idx)]
        dos = dos.drop(columns=col)
        cates.append(cate)

    #     for i in cols:
    #         dos[i]=np.NAN

        # print(len(cate))
        if len(cate) == 0 or len(dos.columns) == 0:
            break

        df = pd.concat(cates).reset_index(drop=True)

        return df

    
def nearestdistances(data_mandiri, data_bvt, distance):
    '''
    df1=pd.read_excel("/Users/jenhar/Downloads/Data Structure & Dummy - Bank Mandiri.xlsx","new dummy")
    df2=gpd.read_file('/Users/jenhar/Downloads/Mandiri Category Sample.geojson')
    df1=df1.rename(columns={'longitude':'lon', 'latitude':'lat'})
    df2=df2.rename(columns={'longitude':'lon', 'latitude':'lat'})
    
    '''

    df1 = data_mandiri.copy()
    df2 = data_bvt.copy()

    cates = []
    dos = df2.apply(lambda row: matrix_distance(
        df1, row['lat'], row['lon']), axis=1)

    while True:

        #     df2=df2[~df2.index.isin(idxs)]
        #     dos=dos[~dos.index.isin(idxs)]
        #     dos=dos.drop(columns=cols)

        df2['distance'] = np.nanmin(dos.to_numpy(), axis=1)
        df2['name'] = dos.idxmin(axis=1)

        cate = df2[df2['distance'] < distance].sort_values(
            'distance').drop_duplicates('name')
        col = cate['name'].values.tolist()
        idx = cate.index.values.tolist()

    #     for i in col:
    #         cols.append(i)

    #     for i in idx:
    #         idxs.append(i)

        df2 = df2[~df2.index.isin(idx)]
        dos = dos[~dos.index.isin(idx)]
        dos = dos.drop(columns=col)
        cates.append(cate)

    #     for i in cols:
    #         dos[i]=np.NAN

        # print(len(cate))
        if len(cate) == 0 or len(dos.columns) == 0:
            

            df = pd.concat(cates).reset_index(drop=True)
            df1['index'] = df1.index

            df = df1.merge(df[['poi_name', 'spatial_score', 'name']],
                           how='left', left_on=df1['index'], right_on=df['name']).fillna(0)
            # df=df.merge(df1, how='left', left_on='name', right_on=df1.index)

            return df
        
            break



