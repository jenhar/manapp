import streamlit as st
import numpy as np
from streamlit_folium import folium_static


def general(gdf_bf, gdf_loc):

    print(gdf_bf, gdf_loc)
    # atm = functions.POI_Catch(
    #     gdf_bf, col_name='nama_sub_kategori', category=['Bank', 'ATM'])

    # atm['keterangan'] = np.where(atm.nama_merchant.str.lower(
    # ).str.contains('mandiri'), 'Mandiri', 'Competitor')

    # cm = functions.LokasiCityMap(gdf_bf, gdf_loc)
    # teritory = functions.Teriroty(atm, gdf_bf, gdf_loc)
    # teritory2 = functions.Teriroty2(atm, gdf_bf, gdf_loc)

    # st.header("General Analytics")
    # col1, col2 = st.columns([1, 1])
    # with col1:
    #     st.caption("Analisis dilakukan di 2 Outlet Mandiri yaitu Mandiri cabang Kramatjati dan Mandiri cabang Menara Indomart.\nMandiri Cabang Kramatjati berada pada wilayah Jakarta Timur sedangkan Mandiri cabang Menara Indomart berada di wilayah Jakarta Utara. Analisis dilakukan dengan melakukan buffer sejauh 2 KM dimana dalam radius 2 KM tersebut, Mandiri cabang Kramatjati mencakup 14 Desa dan 7 Kecamatan sedangkan Mandiri cabang menara Indomart mencakup 6 desa dan 3 kecamatan.")
    # with col2:
    #     st.pydeck_chart(cm)

    # col3, col4 = st.columns([1, 1])
    # with col3:
    #     st.subheader("Analisis Berdasarkan Teritory")
    #     st.markdown(
    #         """
    #             - Cabang Menara Indomart:
    #                 \n
    #                 Terdapat 8 Bank dan ATM Mandiri dengan 56 Competitor dalam radius 2 KM, sedangkan
    #             - Cabang Kramatjati:
    #                 \n
    #                 Terdapat 27 Aset Mandiri (23 ATM dan 4 Bank) dengan 83 Kompetitor
    #         """
    #     )
    # with col4:
    #     folium_static(teritory[0], height=400)

    # col5, col6 = st.columns([1, 1])
    # with col5:
    #     st.plotly_chart(teritory2[1][0])
    # with col6:
    #     st.plotly_chart(teritory2[1][1])
