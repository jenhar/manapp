# Libraries
import pydeck as pdk
from shapely.geometry import mapping
import geopandas as gpd
import streamlit as st
import folium
from streamlit_folium import st_folium
from streamlit_folium import folium_static

from module.fetch_module import fetchData
from module.analytics_module import gdf_loc, catchment
from module.visualization_module import teritory_chart, teritory_map, poi_chart, poi_map, ses_chart, ses_map, demog_chart_all, demog_chart_perdesa, demog_chart_spesific, demog_map_all, demog_map_general, demog_map_per_desa, demog_map_spesific, mw_chart_heatmap, mw_chart_hours, mw_chart_segmenttime, mw_chart_timeseries, mw_chart_weekdays

import pydeck as pdk
from pathlib import Path

# Global Variables
theme_plotly = None  # None or streamlit
week_days = ['Monday', 'Tuesday', 'Wednesday',
             'Thursday', 'Friday', 'Saturday', 'Sunday']

# Config
st.set_page_config(page_title='ESDA',
                   page_icon=':chart_with_upwards_trend:', layout='wide')

# Title
st.title('Exploratory Spatial Data Analytics')
# st.text('Data Analyst: Adelia Sekarsari')
# st.markdown(
#     """
# Locations :
# - Mandiri Cabang Keramatjati
# - Mandiri Cabang Menara Indomaret
# """
# )


# Fetch Data
list_male = ['LK_15_19', 'LK_20_24', 'LK_25_29', 'LK_30_34',
             'LK_35_39', 'LK_40_44', 'LK_45_49', 'LK_50_54', 'LK_55_59']
list_female = ['PR_15_19', 'PR_20_24', 'PR_25_29', 'PR_30_34',
               'PR_35_39', 'PR_40_44', 'PR_45_49', 'PR_50_54', 'PR_55_59']
list_variable = list_male+list_female

data = fetchData(
    Path(__file__).parents[1]/'data/df_poi.geojson',
    Path(__file__).parents[1]/'data/df_poi_atm.geojson',
    Path(__file__).parents[1]/'data/df_demografi.geojson',
    Path(__file__).parents[1]/'data/df_ses.geojson',
    Path(__file__).parents[1]/'data/df_mw.parquet',
    Path(__file__).parents[1]/'data/df_grid.geojson',
    list_variable
)

df_poi, df_poi_atm, df_demog, df_ses, df_mw, df_grid, list_variable = data

branch = st.selectbox(
    'Please select a branch',
    ('Mandiri Cabang Keramatjati', 'Mandiri Cabang Menara Indomaret'))

# poi1
if (branch == 'Mandiri Cabang Keramatjati'):
    longitude = 106.870199
    latitude = -6.295201
    id_ = 'Mandiri Kramatjati'
elif (branch == 'Mandiri Cabang Menara Indomaret'):
    longitude = 106.738968
    latitude = -6.109871
    id_ = 'Mandiri Menara Indomaret'

# create geodataframe from longitude to latitude
loc = gdf_loc(longitude, latitude, id_)

# define projection
proj = 'epsg:32748'

# get catchment based on radius
catch = catchment(loc, 2000)


tab1, tab2, tab3, tab4, tab5 = st.tabs(
    ["General", "Point of Interest", "Social Economic Status", "Demography", "Telco Data"])
with tab1:
    st.header("General")
    col1, col2 = st.columns(2)
    with col1:
        plot = teritory_chart(df_poi_atm, catch)
        st.plotly_chart(plot, use_container_width=True)

    with col2:
        map = teritory_map(df_poi_atm, catch, loc)
        folium_static(map, height=500)
with tab2:
    st.header("Analytics by POI")
    col1, col2 = st.columns(2)
    with col1:
        # POI Chart
        chart_poi = poi_chart(data[0], catch)
        st.plotly_chart(chart_poi, use_container_width=True)

    with col2:
        map_poi = poi_map(data[0], catch, loc)
        # Create a legendQ
        legend_html = '''
        <div style="position: fixed; 
            bottom: 50px; left: 50px; width: 100px; height: 90px; 
            border:2px solid grey; z-index:9999; font-size:14px;
            ">&nbsp; Legend <br>
            &nbsp; Marker 1 &nbsp; <i class="fa fa-map-marker fa-2x"
                        style="color:green"></i><br>
            &nbsp; Marker 2 &nbsp; <i class="fa fa-map-marker fa-2x"
                        style="color:red"></i><br>
            &nbsp; Marker 3 &nbsp; <i class="fa fa-map-marker fa-2x"
                        style="color:blue"></i>
        </div>
        '''

        # Add the legend to the map
        map_poi.get_root().html.add_child(folium.Element(legend_html))

        folium_static(map_poi, height=700)

with tab3:
    st.header("Analytics by SES")
    col1, col2 = st.columns(2)
    with col1:
        # POI Chart
        chart_ses = ses_chart(data[3], catch)
        st.plotly_chart(chart_ses, use_container_width=True)

    with col2:
        map_ses = ses_map(data[3], catch, loc)
        folium_static(map_ses, height=500)

with tab4:
    st.header("Analytics by Demography")
    col1, col2 = st.columns(2)
    with col1:
        # POI Chart
        st.plotly_chart(demog_chart_all(df_demog, catch,
                        list_variable), use_container_width=True)

    with col2:
        folium_static(demog_map_all(df_demog, catch, loc), height=500)

    col3, col4 = st.columns(2)
    with col3:
        st.plotly_chart(demog_chart_spesific(df_demog, catch,
                        list_variable), use_container_width=True)

    with col4:
        folium_static(demog_map_spesific(
            df_demog, catch, loc, list_variable), height=500)

with tab5:
    st.header("Analytics by Telco Data")

    @st.cache_data
    def getData():
        grid = gpd.read_file(Path(__file__).parents[1]/"data/grid.geojson").astype({'time': 'str'})
        line = gpd.read_file(Path(__file__).parents[1]/"data/line.geojson").astype({'time': 'str'})
        point = gpd.read_file(Path(__file__).parents[1]/"data/point.geojson")
        point['coordinates'] = point['geometry'].apply(lambda x: [x.x, x.y])
        point['radius'] = point['ratio'].apply(lambda x: x*100)
        return grid, line, point

    colMenu, colMap = st.columns(2)

    with colMenu:
        dates = st.selectbox(
            "Choose date", ['2022-10-17']
        )

        layer = st.multiselect(
            'Layer',
            ['Grid Density', 'Flow Volume', 'Flow Mobility'],
            ['Grid Density', 'Flow Volume', 'Flow Mobility'])

        COLOR_RANGE = [
            [65, 182, 196],
            [127, 205, 187],
            [199, 233, 180],
            [237, 248, 177],
            [255, 255, 204],
            [255, 237, 160],
            [254, 217, 118],
            [254, 178, 76],
            [253, 141, 60],
            [252, 78, 42],
            [227, 26, 28],
            [189, 0, 38],
            [128, 0, 38],
        ]

        def color_scale(val, BREAKS):
            for i, b in enumerate(BREAKS):
                if val < b:
                    return COLOR_RANGE[i]
            return COLOR_RANGE[i]

        if not dates:
            st.error("Please select date.")
        else:
            grid, line, point = getData()
            center = grid.unary_union.centroid
            times = grid.time.unique()
            timeSelected = st.select_slider("time", options=times)
            gridSelected = grid[grid.time == timeSelected]
            gridSelected = gridSelected.to_crs('epsg:4326')
            gridSelected = gpd.sjoin(gridSelected, catch[['id', 'geometry']])

            lineSelected = line[line.time == timeSelected]
            lineSelected = lineSelected.to_crs('epsg:4326')
            lineSelected = gpd.sjoin(
                lineSelected, gridSelected[['id', 'geometry']])

            point = point.to_crs('epsg:4326')
            point = gpd.sjoin(point, gridSelected[['id', 'geometry']])

        custom_scale = (gridSelected['counts'].quantile(
            (0, 0.2, 0.4, 0.6, 0.8, 1))).tolist()
        gridSelected["fill_color"] = gridSelected["counts"].apply(
            lambda row: color_scale(row, BREAKS=custom_scale))
        gridSelected['coordinates'] = gridSelected['geometry'].apply(
            lambda x: mapping(x)['coordinates'])
        lineSelected["from_coordinates"] = lineSelected["geometry"].apply(
            lambda x: [x.coords[0][0], x.coords[0][1]])
        lineSelected["to_coordinates"] = lineSelected["geometry"].apply(
            lambda x: [x.coords[1][0], x.coords[1][1]])
        layers = []

        if 'Grid Density' in layer:
            layers.append(pdk.Layer(
                'GeoJsonLayer',
                gridSelected.__geo_interface__,
                opacity=0.8,
                stroked=False,
                filled=True,
                extruded=False,
                wireframe=True,
                get_elevation='properties.counts / 20',
                get_fill_color='properties.fill_color',
                get_line_color=[255, 255, 255],
                pickable=True
            ))
        if 'Flow Volume' in layer:
            layers.append(pdk.Layer(
                "ScatterplotLayer",
                point,
                pickable=True,
                opacity=0.8,
                stroked=True,
                filled=True,
                radius_scale=6,
                radius_min_pixels=1,
                radius_max_pixels=100,
                line_width_min_pixels=1,
                get_position="coordinates",
                get_radius="radius",
                get_fill_color=[255, 140, 0],
                get_line_color=[0, 0, 0],
            )
            )
        if 'Flow Mobility' in layer:
            layers.append(pdk.Layer(
                "ArcLayer",
                lineSelected,
                pickable=True,
                get_width=1,
                get_stroke_width=12,
                get_source_position="from_coordinates",
                get_target_position="to_coordinates",
                get_source_color=[64, 255, 0],
                get_target_color=[0, 128, 200],
                auto_highlight=True,
                picking_radius=10,
            )
            )
    with colMap:
        st.pydeck_chart(pdk.Deck(
            map_style=None,
            initial_view_state=pdk.ViewState(
                latitude=center.y,
                longitude=center.x,
                zoom=9,
            ),
            layers=layers,
            tooltip={"text": "index: {index} \n counts: {counts} \n total_flow: {total_flow} \n origin: {origin} \n destination: {destination} \n flow: {flows}"},))

    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(mw_chart_timeseries(
            catch, df_grid,  df_mw), use_container_width=True)
    with col2:
        st.plotly_chart(mw_chart_hours(catch, df_grid,  df_mw),
                        use_container_width=True)

    col3, col4 = st.columns(2)
    with col3:
        st.plotly_chart(mw_chart_segmenttime(
            catch, df_grid,  df_mw), use_container_width=True)
    with col4:
        st.plotly_chart(mw_chart_weekdays(
            catch, df_grid,  df_mw), use_container_width=True)

    st.plotly_chart(mw_chart_heatmap(catch, df_grid,  df_mw),
                    use_container_width=True)

# Style
with open(Path(__file__).parents[1]/'style.css')as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

make_map_responsive = """
 <style>
 [title~="st.iframe"] { width: 100%}
 </style>
"""
st.markdown(make_map_responsive, unsafe_allow_html=True)
