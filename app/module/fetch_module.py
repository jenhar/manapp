import geopandas as gpd
import pandas as pd
import numpy as np
import streamlit as st


@st.cache_data
def fetchData(poi, poi_atm, demografi, ses, mobilewalla, grid, list_variable):

    df_poi = gpd.read_file(poi)

    df_poi_atm = gpd.read_file(poi_atm)
    df_poi_atm['keterangan'] = np.where(df_poi_atm.nama_merchant.str.lower(
    ).str.contains('mandiri'), 'Mandiri', 'Competitor')
    df_poi_atm['Description'] = df_poi_atm['keterangan']

    df_demog = gpd.read_file(demografi, crs='epsg:4326')
    df_ses = gpd.read_file(ses)
    df_mw = pd.read_parquet(mobilewalla)
    df_grid = gpd.read_file(grid)

    st.session_state["df_poi"] = df_poi
    st.session_state["df_poi_atm"] = df_poi_atm
    st.session_state["df_demog"] = df_demog
    st.session_state["df_ses"] = df_ses
    st.session_state["df_mw"] = df_mw
    st.session_state["df_grid"] = df_grid
    st.session_state["list_variable"] = list_variable

    return df_poi, df_poi_atm, df_demog, df_ses, df_mw, df_grid, list_variable
