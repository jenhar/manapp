#from typing import OrderedDict
from module.whitespace_distance import nearestdistances, creategeom, setgeom, setlonlat, nlp_value, mandiri_score, spatial_score, categori_type
from module.whitespace_distance import nearestdistances, creategeom, setgeom, setlonlat, nlp_value
#from tkinter.tix import COLUMN
#from turtle import width
import streamlit as st
import pandas as pd
import geopandas as gpd
import folium
#from sklearn.preprocessing import MinMaxScaler
from streamlit_folium import st_folium
#from folium.plugins import Draw
#from shapely.geometry import Point
from module.analytics_module import gdf_loc, catchment
from streamlit_folium import folium_static
import numpy as np
from folium.plugins import FloatImage
from st_aggrid import GridOptionsBuilder, AgGrid, GridUpdateMode, DataReturnMode



def customer_order(d4):
    d4=d4.sort_values(by=['spatial_score','mandiri_score'],
                      ascending = [False, True]).head(200).reset_index(drop=True)
    #d4['no']=d4.index+1
    
    return d4

def noncustomer_order(d4):
    d4=d4.sort_values(by=['spatial_score'],
                      ascending = [False]).head(200).reset_index(drop=True)
    #d4['no']=d4.index+1
    
    return d4

    
    
def undifind_order(d4):
    d4=d4.sort_values(by=['mandiri_score'],
                      ascending = [True]).head(200).reset_index(drop=True)
    #d4['no']=d4.index+1
    
    return d4
    

st.set_page_config(page_title='POI RECOMENDATION DASBOARD',
                   layout="wide")

st.title(":bar_chart: POI Dashboard")
st.sidebar.header("Filter: ")

# Branch Selections
branch = st.sidebar.selectbox(
    'Please select a branch',
    ('Mandiri Cabang Keramatjati', 'Mandiri Cabang Menara Indomaret'), index=0)

# poi1
if (branch == 'Mandiri Cabang Keramatjati'):
    longitude = 106.870199
    latitude = -6.295201
    id_ = 'Mandiri Kramatjati'
elif (branch == 'Mandiri Cabang Menara Indomaret'):
    longitude = 106.738968
    latitude = -6.109871
    id_ = 'Mandiri Menara Indomaret'

st.session_state['center_lon'] = longitude
st.session_state['center_lat'] = latitude

loc = gdf_loc(longitude, latitude, id_)
proj = 'epsg:4326'
catch = catchment(loc, 2000)


@ st.cache_data
def getData():
    data = gpd.read_file("/data/mandiri_category.geojson")
    return data


data = getData()
data = data.to_crs('epsg:4326')
data = gpd.sjoin(data, catch[['id', 'geometry']])
data = data.reset_index(drop=True)

st.session_state['data'] = data

analyticsType = st.sidebar.radio(
    'Analytics based on',
    ('Postal Code', 'Merchant'))
st.session_state['analyticsType'] = analyticsType


if st.session_state['analyticsType'] == 'Merchant':

    # filterMode = st.sidebar.radio(
    #     "Please select a Filter",
    #     ('Group', 'Category'))

    if (branch == 'Mandiri Cabang Keramatjati'):
        df1 = pd.read_excel('/data/keramatjati_merchant.xls', 'sheet1')

    else:
        df1 = pd.read_excel('/data/pik_merchant.xls', 'sheet1')

    #st.session_state['filterMode'] = filterMode
if st.session_state['analyticsType'] == 'Postal Code':
    st.session_state['filterMode'] = 'Group'

    if (branch == 'Mandiri Cabang Keramatjati'):
        df1 = pd.read_excel('/data/keramatjati_kodepodes.xls', 'sheet1')

    else:
        df1 = pd.read_excel('/data/pik_kodepodes.xls', 'sheet1')

df1['geom'] = [creategeom(x) for x in df1['lonlat']]
df1 = setgeom(df1)
setlonlat(df1)
df1.crs=catch.crs
df1 = gpd.sjoin(df1, catch[['id', 'geometry']])
df1 = df1.reset_index(drop=True)
d1 = spatial_score(data)
df1 = mandiri_score(df1)
df = nearestdistances(df1, d1, 100)
df = df.rename(columns={'geom': 'geometry'})
d11 = d1[~d1.index.isin(df['name_y'].values.tolist())]
nlp_value(df, 'name_x', 'poi_name')
m = df[['buc', 'branch', 'is_deposit', 'is_giro', 'is_tabungan', 'flag_mcm1', 'flag_mcm2', 'flag_mgt', 'flag_mib',
        'flag_scm', 'online_using_rate', 'name_x', 'poi_name', 'nlp_score', 'mandiri_score', 'spatial_score', 'geometry']]
b = d11[['poi_name', 'spatial_score', 'geometry']]
dfinal = pd.concat([m, b]).reset_index(drop=True)
dfinal = dfinal.fillna(0)
dfinal=dfinal.rename(columns={'name_x':'name'})
dfinal = dfinal.set_geometry('geometry')
dfinal['type'] = [categori_type(n, m, s) for n, m, s in zip(
    dfinal['nlp_score'], dfinal['mandiri_score'], dfinal['spatial_score'])]
#dfinal = dfinal.sort_values(by='spatial_score', ascending=False)
#dfinal = dfinal.sort_values(by='mandiri_score', ascending=True)

dfinal=dfinal.sort_values(by=['spatial_score','mandiri_score'],
               ascending = [False, True]).reset_index(drop=True)
#dfinal = dfinal.reset_index(drop=True)
dfinal['no'] = dfinal.index+1
dfinal = dfinal[['no'] + [col for col in dfinal.columns if col != 'no']]
# dfinal = dfinal.sort_values('spatial_score', ascending=False)

#tanda1
# categoryOpts = df1['group'].unique()
# categoryOpts = np.append('All Group', categoryOpts)
# subCategoryOpts = data['mandiri_subcategory'].unique().tolist()
# subCategoryOpts = np.append('All Category', subCategoryOpts)

# if st.session_state['filterMode'] == "Group":
#     st.session_state['options'] = categoryOpts
# elif st.session_state['filterMode'] == "Category":
#     st.session_state['options'] = subCategoryOpts

# filterValue = st.sidebar.selectbox(
#     'Pelase select Group or Category',
#     (st.session_state['options']))

# st.session_state['filterValue'] = filterValue

# if st.session_state['filterMode'] == "Group" and st.session_state['filterValue'] != "All Category":
#     data = data[data['mandiri_category'] == st.session_state['filterValue']]
#     st.session_state['data'] = data

# elif st.session_state['filterMode'] == "Catagory" and st.session_state['filterValue'] != "All Sub Category":
#     data = data[data['mandiri_subcategory'] == st.session_state['filterValue']]
#     st.session_state['data'] = data
#     df1 = df1[data['pengelompokan_merchant_kategori']
#               == st.session_state['filterValue']] 
#tanda1

# st.session_state['total'] = len(data)
# customer = data[data['type'] == 'customer']
# st.session_state['customer'] = len(customer)
# non_customer = data[data['type'] == 'non customer']
# st.session_state['non_customer'] = len(non_customer)
# undefined_customer = data[data['type'] == 'undefined customer']
# st.session_state['undefined_customer'] = len(undefined_customer)
# st.session_state['penetration'] = round(((len(customer)/len(data))*100), 2)

st.session_state['total'] = len(dfinal)
customer = dfinal[dfinal['type'] == 'customer']
st.session_state['customer'] = len(customer)
non_customer = dfinal[dfinal['type'] == 'non customer']
st.session_state['non_customer'] = len(non_customer)
undefined_customer = dfinal[dfinal['type'] == 'undefined customer']
st.session_state['undefined_customer'] = len(undefined_customer)
st.session_state['penetration'] = round(((len(customer)/len(dfinal))*100), 2)


col1, col2, col3, col4, col5 = st.columns(5)
col1.metric("Total", st.session_state['total'])
col2.metric("Customer", st.session_state['customer'])
col3.metric("Non Customer", st.session_state['non_customer'])
col4.metric("Undefined Customer", st.session_state['undefined_customer'])
col5.metric("Customer Penetration", str(st.session_state['penetration'])+'%')


map = folium.Map(location=[st.session_state['center_lat'],
                           st.session_state['center_lon']], zoom_start=14)

icon_map = {
    'customer': 'star',
    'non customer': 'crosshairs',
    'undefined customer': 'crosshairs'
}


def get_icon_color(value):
    if value == 'non customer':
        return 'orange'
    elif value == 'undefined customer':
        return 'red'
    else:
        return 'green'


def get_icon_url(subkategori):
    base_url = './data/assets/poi_icon/'
    icon_name = str(subkategori).split(" ")
    icon_name = '_'.join(icon_name)
    icon_url = f"{base_url}{icon_name}.png"
    return icon_url


# popup_style = '''
#     <p style="color:blue;font-weight:600">{poi_name}</p>
# '''
popup_style = '''
    <h4 style="color:blue;font-weight:600">{poi_name}</h4>
    <p style="color:black;">NLP score: {nlp_score}</p>
    <p style="color:black;">Mandiri score: {mandiri_score}</p>
    <p style="color:black;">Spatial score: {spatial_score}</p>
    <p style="color:black;">Online Using Rate: {online_using_rate}</p>
'''


def iterateMap(map, data):
    for index, row in data.iterrows():
        # if str(row['subkategori_v2']) != 'nan' and str(row['subkategori_v2']) != ' ':
        #     popup_content = popup_style.format(
        #         brand_name=row['brand_name'], subkategori=row['subkategori_v2'], type=row['type'])
        #     icon_url = get_icon_url(row['subkategori_v2'])
        #     icon = folium.features.CustomIcon(icon_url, icon_size=(24, 24))
        #     marker = folium.Marker(
        #         [row.geometry.y, row.geometry.x], popup=folium.Popup(popup_content), icon=icon)
        #     marker.add_to(map)
        if str(row['type']) == 'non customer':
            icon_name = icon_map.get(row['type'], 'circle')
            color = get_icon_color(row['type'])
            icon = folium.Icon(icon=icon_name, prefix='fa',
                               color=color, size=(20, 20))
            popup_content = popup_style.format(
                poi_name=row['name'],
                nlp_score=row['nlp_score'],
                mandiri_score=row['mandiri_score'],
                spatial_score=row['spatial_score'],
                online_using_rate=row['online_using_rate'],
            )
            marker = folium.Marker(
                [row.geometry.y, row.geometry.x],
                popup=folium.Popup(popup_content),
                icon=icon)
            marker.add_to(map)
        if str(row['type']) == 'undefined customer':
            icon_name = icon_map.get(row['type'], 'circle')
            color = get_icon_color(row['type'])
            icon = folium.Icon(icon=icon_name, prefix='fa',
                               color=color, size=(20, 20))
            popup_content = popup_style.format(
                poi_name=row['name'],
                nlp_score=row['nlp_score'],
                mandiri_score=row['mandiri_score'],
                spatial_score=row['spatial_score'],
                online_using_rate=row['online_using_rate'],
            )
            marker = folium.Marker(
                [row.geometry.y, row.geometry.x],
                popup=folium.Popup(popup_content),
                icon=icon)
            marker.add_to(map)
        if str(row['type']) == 'customer':
            icon_name = icon_map.get(row['type'], 'circle')
            color = get_icon_color(row['type'])
            icon = folium.Icon(icon=icon_name, prefix='fa',
                               color=color, size=(20, 20))
            popup_content = popup_style.format(
                poi_name=row['name'],
                nlp_score=row['nlp_score'],
                mandiri_score=row['mandiri_score'],
                spatial_score=row['spatial_score'],
                online_using_rate=row['online_using_rate'],
            )
            marker = folium.Marker(
                [row.geometry.y, row.geometry.x],
                popup=folium.Popup(popup_content),
                icon=icon)
            marker.add_to(map)


loc_icon_url = "./data/assets/poi_icon/marker-mandiri.png"
loc_icon = folium.features.CustomIcon(loc_icon_url, icon_size=(48, 48))
loc_marker = folium.Marker([st.session_state['center_lat'],
                            st.session_state['center_lon']], icon=loc_icon).add_to(map)

CatchLayer = folium.GeoJson(data=catch)
# Add GeoJson layer to map
CatchLayer.add_to(map)

legend_url = "https://i.ibb.co/6B4fDyj/poi-legend.png"
legend = FloatImage(legend_url, bottom=5, left=5, size=(50, 50)).add_to(map)


def AgGridClick(data):

    gb = GridOptionsBuilder.from_dataframe(data)
    gb.configure_side_bar()  # Add a sidebar
    gb.configure_column('no', width=70)
    gb.configure_column('nlp_score', width=120)
    gb.configure_column('mandiri_score', width=120)
    gb.configure_column('spatial_score', width=120)
    gb.configure_column('online_using_rate', width=120)
    gb.configure_column('type', width=140)
    gb.configure_column('name', width=210)
    gb.configure_selection('multiple', use_checkbox=True,
                           groupSelectsChildren="Group checkbox select children")  # Enable multi-row selection
    gridOptions = gb.build()
    # gridOptions['defaultSortModel'] = [
    #     {"colId": "sptaial_score", "sort": "asc"}]
    # gridOptions['defaultSortModel'] = [
    #     {"colId": "mandiri_score", "sort": "dsc"}]

    selected = AgGrid(data,
                      gridOptions=gridOptions,
                      data_return_mode='AS_INPUT',
                      update_mode='MODEL_CHANGED',
                      fit_columns_on_grid_load=False,
                      enable_enterprise_modules=True,
                      width='100%',
                      #   reload_data=True,
                      height=500)
    locSelected = selected['selected_rows']
    dfSelected = pd.DataFrame(locSelected)
    return dfSelected


def get_icon_table(value):
    if value == 0:
        return '❌'
    elif value == 1:
        return '✅'


def get_percent(value):
    percent = str(value*100)+'%'
    return percent


colTable, colMap = st.columns(2)
# field = ['type', 'name_x', 'poi_name', 'nlp_score', 'mandiri_score', 'spatial_score', 'online_using_rate', 'buc', 'branch', 'is_deposit', 'is_giro', 'is_tabungan', 'flag_mcm1', 'flag_mcm2', 'flag_mgt', 'flag_mib', 'flag_scm']
field = ['no', 'type', 'name', 'poi_name', 'nlp_score', 'mandiri_score',
         'spatial_score', 'online_using_rate']
with colTable:
    selectType = st.selectbox(
        'Please Select Customer Type',
        ('All Customer', 'Customer', 'Non Customer', 'Undefined Customer'))
    st.session_state['customer_type'] = selectType
    if selectType == 'All Customer':
        st.session_state['data'] = dfinal
        selectedRow = AgGridClick(
            dfinal[field])
        st.session_state['selected_rows'] = selectedRow
        if len(st.session_state['selected_rows']) == 0:
            iterateMap(map, st.session_state['data'])
        else:
            filterData = st.session_state['data'].loc[st.session_state['data']['no'].isin(
                st.session_state['selected_rows']['no'])]
            # dfinal = filterData
            st.session_state['data'] = filterData
            iterateMap(map, st.session_state['data'])

    elif selectType == 'Customer':
        filteredByType = dfinal[dfinal['type'] == 'customer']
        filteredByType = customer_order(filteredByType)
        st.session_state['data'] = filteredByType

        selectedRow = AgGridClick(
            filteredByType[field])
        st.session_state['selected_rows'] = selectedRow

        if len(st.session_state['selected_rows']) == 0:
            iterateMap(map, st.session_state['data'])
        else:
            filterData = st.session_state['data'].loc[st.session_state['data']['no'].isin(
                st.session_state['selected_rows']['no'])]
            # dfinal = filterData
            st.session_state['data'] = filterData
            iterateMap(map, st.session_state['data'])
    elif selectType == 'Non Customer':
        filteredByType = dfinal[dfinal['type'] == 'non customer']
        filteredByType = noncustomer_order(filteredByType)
        st.session_state['data'] = filteredByType

        selectedRow = AgGridClick(
            filteredByType[field])
        st.session_state['selected_rows'] = selectedRow

        if len(st.session_state['selected_rows']) == 0:
            iterateMap(map, st.session_state['data'])
        else:
            filterData = st.session_state['data'].loc[st.session_state['data']['no'].isin(
                st.session_state['selected_rows']['no'])]
            # data = filterData
            st.session_state['data'] = filterData
            iterateMap(map, st.session_state['data'])
    elif selectType == 'Undefined Customer':
        filteredByType = dfinal[dfinal['type'] == 'undefined customer']

        filteredByType = undifind_order(filteredByType)
        st.session_state['data'] = filteredByType

        selectedRow = AgGridClick(
            filteredByType[field])
        st.session_state['selected_rows'] = selectedRow

        if len(st.session_state['selected_rows']) == 0:
            iterateMap(map, st.session_state['data'])
        else:
            filterData = st.session_state['data'].loc[st.session_state['data']['no'].isin(
                st.session_state['selected_rows']['no'])]
            # data = filterData
            st.session_state['data'] = filterData
            iterateMap(map, st.session_state['data'])
with colMap:
    folium_static(map, width=800, height=600)

if len(st.session_state['selected_rows']) > 0:
    dfinalFilter = dfinal.drop('geometry', axis=1)
    dfinalFilter = dfinalFilter[dfinalFilter['no'].isin(
        list(st.session_state['selected_rows']['no']))]
    

    dfinalFilter['is_giro'] = dfinalFilter['is_giro'].apply(get_icon_table)
    dfinalFilter['is_deposit'] = dfinalFilter['is_deposit'].apply(
        get_icon_table)
    dfinalFilter['is_tabungan'] = dfinalFilter['is_tabungan'].apply(
        get_icon_table)
    dfinalFilter['flag_mcm1'] = dfinalFilter['flag_mcm1'].apply(get_icon_table)
    dfinalFilter['flag_mcm2'] = dfinalFilter['flag_mcm2'].apply(get_icon_table)
    dfinalFilter['flag_mgt'] = dfinalFilter['flag_mgt'].apply(get_icon_table)
    dfinalFilter['flag_mib'] = dfinalFilter['flag_mib'].apply(get_icon_table)
    dfinalFilter['flag_scm'] = dfinalFilter['flag_scm'].apply(get_icon_table)
    dfinalFilter['online_using_rate'] = dfinalFilter['online_using_rate'].apply(
        get_percent)
    dfinalFilter = dfinalFilter.reset_index(drop=True)
    st.table(dfinalFilter)


with open('style.css')as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
make_map_responsive = """
 <style>
 [title~="st.iframe"] { width: 100%}
 </style>
"""
st.markdown(make_map_responsive, unsafe_allow_html=True)
