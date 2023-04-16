import geopandas as gpd
import pandas as pd
import numpy as np
import folium
import matplotlib.colors as colors
import plotly.express as px
import plotly.graph_objs as go


def teritory_map(gdf_atm, gdf_catch, gdf_loc):
    # color1 = [50, 82, 133]
    # color2 = [253, 210, 18]
    color1 = '#325285'
    color2 = '#FDD212'

    # view_state = pdk.ViewState(
    #     latitude=gdf_loc.lat[0],
    #     longitude=gdf_loc.lon[0],
    #     zoom=13,
    #     bearing=0,
    #     pitch=0
    # )

    # base_layer = pdk.Layer(
    #     "TileLayer",
    #     data=None,
    #     opacity=0.9,
    #     getTileData="https://a.basemaps.cartocdn.com/rastertiles/voyager/{z}/{x}/{y}.png"
    # )

    # layer_catch = pdk.Layer(
    #     'GeoJsonLayer',
    #     data=gdf_catch,
    #     opacity=0.4,
    #     get_fill_color=color1,
    #     stroked=True,
    #     get_line_color='grey',
    #     get_line_width=2,
    #     pickable=True
    # )

    # gdf_atm["lat"] = gdf_atm.geometry.y
    # gdf_atm["lon"] = gdf_atm.geometry.x

    # # define function to get color based on keterangan
    # def get_color(row):
    #     if row['keterangan'] == 'Competitor':
    #         return color2
    #     else:
    #         return color1

    # # create new column with colors based on keterangan
    # gdf_atm['color'] = gdf_atm.apply(lambda row: get_color(row), axis=1)

    # layer_atm = pdk.Layer(
    #     'ScatterplotLayer',
    #     data=gdf_atm,
    #     get_position=["lon", "lat"],
    #     get_radius=50,
    #     get_fill_color="color",
    #     get_line_color=[0, 0, 0],
    #     pickable=True,
    #     auto_highlight=True
    # )

    # # print(gdf_atm)
    # gdf_loc["icon"] = "./assets/iconmap/marker-mandiri.png"

    # # abs_path = os.path.abspath("./assets/iconmap/marker-mandiri.png")
    # # ICON_URL = "file://" + abs_path
    # ICON_URL = "https://i.ibb.co/C26gt6R/marker-mandiri.png"

    # icon_data = {
    #     "url": ICON_URL,
    #     "width": 128,
    #     "height": 128,
    #     "anchorY": 128
    # }

    # gdf_loc["icon_data"] = None
    # for i in gdf_loc.index:
    #     gdf_loc["icon_data"][i] = icon_data

    # layer_loc = pdk.Layer(
    #     "IconLayer",
    #     data=gdf_loc,
    #     get_position=['lon', 'lat'],
    #     get_size=6,
    #     get_icon="icon_data",
    #     get_color=[253, 210, 18],
    #     size_scale=6,
    #     pickable=True,
    #     auto_highlight=True,
    #     # tooltip=tooltip_loc
    # )

    # layers = [base_layer, layer_catch, layer_atm, layer_loc],

    # map = pdk.Deck(
    #     layers=layers,
    #     initial_view_state=view_state,
    #     map_style='mapbox://styles/mapbox/light-v9'
    # )

    # # Create a Streamlit checkbox for each layer to control visibility
    # layer_visibility = {}
    # for layer in layers:
    #     layer_name = layer
    #     layer_visibility[layer_name] = st.checkbox(layer_name, value=True)

    # # Filter the layers based on the checkbox values
    # visible_layers = [
    #     layer for layer in layers if layer_visibility[layer.get_name()]]

    # # Update the PyDeck Deck object with the filtered layers
    # map.layers = visible_layers
    # return map

    # Map Visualization
    m = gdf_catch.explore(
        tiles='Cartodb Positron',
        style_kwds=dict(color='grey', opacity=0.4)
    )
    gdf_atm.explore(
        m=m,
        column='Description',
        cmap=colors.ListedColormap([color2, color1]),
        style_kwds=dict(radius=4.5),
        tooltip=['nama_merchant', 'Description']
    )
    import folium
    geo_df_list = [[point.xy[1][0], point.xy[0][0]]
                   for point in gdf_loc.geometry]
    for i, coordinates in enumerate(geo_df_list):
        folium.Marker(
            location=coordinates,
            icon=folium.Icon(color="darkblue", icon_color='#FDD212',
                             icon="fa-university", prefix='fa'),
            popup="Location : " + str(gdf_catch.reset_index()['id'][i])
        ).add_to(m)
    return m


def teritory_chart(gdf_atm, gdf_catch):
    color1 = '#325285'
    color2 = '#FDD212'
    gdf_atm = gdf_atm.set_crs('epsg:4326')
    poi = gpd.sjoin(gdf_atm, gdf_catch[['id', 'geometry']])

    for i in poi.id.unique().tolist():
        poi_i = poi[poi['id'] == i].reset_index()
        group = poi_i.groupby(['nama_sub_kategori', 'Description'])[
            'id_merchant'].count().reset_index()
        fig = px.bar(group, x="nama_sub_kategori", y="id_merchant",
                     color='Description', barmode='group', text='id_merchant',
                     color_discrete_map={
                         'Competitor': color2,
                         'Mandiri': color1},
                     title='Total ATM and Bank in Catchment Area, '+str(i),
                     height=500)
        fig.update_traces(marker_line_color='white',
                          marker_line_width=3, )
        fig.update_layout(xaxis_title="Category",
                          yaxis_title="Total POI")
    return fig


def hex_to_RGB(hex_str):
    """ #FFFFFF -> [255,255,255]"""
    # Pass 16 to the integer function for change of base
    return [int(hex_str[i:i+2], 16) for i in range(1, 6, 2)]


def get_color_gradient(c1, c2, n):
    """
    Given two hex colors, returns a color gradient
    with n colors.
    """
    assert n > 1
    c1_rgb = np.array(hex_to_RGB(c1))/255
    c2_rgb = np.array(hex_to_RGB(c2))/255
    mix_pcts = [x/(n-1) for x in range(n)]
    rgb_colors = [((1-mix)*c1_rgb + (mix*c2_rgb)) for mix in mix_pcts]
    return ["#" + "".join([format(int(round(val*255)), "02x") for val in item]) for item in rgb_colors]


def ses_map(gdf_ses, gdf_catch, gdf_loc):
    gdf_join = gpd.sjoin(gdf_ses, gdf_catch[['geometry', 'id']])
    gdf_clip = gpd.clip(gdf_ses, gdf_catch)
    pallete = {'High': '#0D2C5B',
               'Medium-High': '#206DAB',
               'Medium-Low': '#FDD212',
               'Low': '#FDF8B3'
               }
    var = []
    not_var = []
    for i in ['High', 'Medium-High', 'Medium-Low', 'Low']:
        if i in gdf_clip.nilai.unique():
            var.append(i)
        else:
            not_var.append(i)
    pal_ = {key: pallete[key] for key in var}
    color = [*pal_.values()]
    m = gdf_clip.explore(
        tiles='Cartodb Positron',
        column='nilai',
        cmap=colors.ListedColormap(color),
        categories=var,
        zoom_start=14
    )
    geo_df_list = [[point.xy[1][0], point.xy[0][0]]
                   for point in gdf_loc.geometry]
    for i, coordinates in enumerate(geo_df_list):
        folium.Marker(
            location=coordinates,
            icon=folium.Icon(color="darkblue", icon_color='#FDD212',
                             icon="fa-university", prefix='fa'),
            popup="Location : " + str(gdf_catch.reset_index()['id'][i])
        ).add_to(m)
    return m


def ses_chart(gdf_ses, gdf_catch, proj='epsg:3395'):
    """Fungsi untuk mendapatkan Chart SES dalam catchment
    """
    # Calculate percentage of SES
    percentage = pd.DataFrame()
    percentage['id_desa'] = []
    percentage['percent'] = []
    x = gpd.clip(gdf_ses, gdf_catch).reset_index()
    percentage['id_desa'] = x.id_desa.unique()
    percentage['percent'] = x.to_crs(proj).area/gdf_catch.to_crs(proj).area[0]

    ses_merge = pd.merge(percentage, gdf_ses[['id_desa', 'nilai']])

    # SES Chart
    for i in gdf_catch.id.unique().tolist():
        group = ses_merge.groupby('nilai')['percent'].sum().reset_index()
        group['percent'] = round(group['percent']*100, 2)
        group.columns = ['nilai', 'percentage']
        data = pd.DataFrame(
            {'SES': ['High', 'Medium-High', 'Medium-Low', 'Low']})
        data2 = pd.merge(data, group, how='left',
                         left_on='SES', right_on='nilai')
        data2 = data2.fillna(0)
        fig = px.bar(data2,
                     height=500,
                     y='percentage',
                     x='SES',
                     text_auto=True,
                     title="SES Percentage in Catchment "+'<b>'+i+'</b>',
                     color='SES',
                     color_discrete_map={
                         'High': '#0D2C5B',
                         'Medium-High': '#206DAB',
                                        'Medium-Low': '#FDD212',
                                        'Low': '#FDF8B3'},
                     category_orders={'nilai': ['High', 'Medium-High', 'Medium-Low', 'Low']

                                      })
        fig.update_xaxes(categoryorder='array',
                         categoryarray=['High', 'Medium-High', 'Medium-Low', 'Low'])
        fig.update_layout(xaxis_title="Sub Category",
                          yaxis_title="Percentage",
                          yaxis_range=[0, 100],
                          )
        return fig


def demog_map_spesific(gdf_demog, gdf_catch, gdf_loc, variable, proj='epsg:3395'):
    color1 = '#0D2C5B'
    color2 = '#FDD212'
    color = get_color_gradient(color1, color2, 6)

    gdf_demog_join = gpd.sjoin(gdf_demog, gdf_catch[['geometry', 'id']])
    # calculate percentage of demog in catchment
    percentage = pd.DataFrame()
    percentage['kode_desa'] = []
    percentage['percent'] = []
    x = gpd.clip(gdf_demog_join, gdf_catch).reset_index()
    y = gdf_demog_join
    percentage['kode_desa'] = x.kode_desa.unique()
    percentage['percent'] = x.to_crs(proj).area/gdf_catch.to_crs(proj).area[0]

    percentage['kode_desa'] = percentage['kode_desa'].astype(str)
    demog_percent = pd.merge(percentage, gdf_demog_join.drop(columns=['id_desa', 'nama_desa',
                                                                      'id_kota', 'nama_kota', 'geometry']), on='kode_desa')
    demog_cal = gdf_demog_join[['kode_desa', 'geometry']].copy()

    columns = demog_percent.columns.tolist()
    variable = variable
    var = []
    not_var = []
    for i in variable:
        if i in columns:
            var.append(i)
        else:
            not_var.append(i)

    for i in var:
        demog_cal[i] = round(demog_percent['percent']*demog_percent[i])

    demog_cal['population'] = demog_cal[var].sum(axis=1)
    demog_cal['id'] = gdf_catch.id.unique().tolist()[0]

    # map visualization
    demografi_clip = gpd.clip(demog_cal, gdf_catch[['geometry']])
    m = gdf_demog_join.explore(tiles='Cartodb Positron',
                               legend=False,
                               style_kwds=dict(color='grey', opacity=0.4))
    demografi_clip.explore(
        m=m,
        zoom_start=14,
        column='population',
        k=5,
        scheme='equalinterval',
        legend_kwds=dict(colorbar=False, fmt='{:.0f}'),
        legend=True,
        cmap='Blues_r'
    )
    geo_df_list = [[point.xy[1][0], point.xy[0][0]]
                   for point in gdf_loc.geometry]
    for i, coordinates in enumerate(geo_df_list):
        folium.Marker(
            location=coordinates,
            icon=folium.Icon(color="darkblue", icon_color='#FDD212',
                             icon="fa-university", prefix='fa'),
            popup="Location : " + str(gdf_catch.reset_index()['id'][i])
        ).add_to(m)
    return m


def demog_map_general(gdf_demog, gdf_catch, gdf_loc):
    color1 = '#0D2C5B'
    color2 = '#FDD212'
    color = get_color_gradient(color1, color2, 6)

    list_var = gdf_demog.drop(columns=[
                              'id_desa', 'nama_desa', 'id_kota', 'nama_kota', 'geometry']).columns.tolist()
    gdf_demog_join = gpd.sjoin(gdf_demog, gdf_catch[['geometry', 'id']])
    gdf_demog_join['population'] = gdf_demog_join[list_var].sum(axis=1)

    # map visualization
    m = gdf_demog_join.explore(tiles='Cartodb Positron',
                               column='population',
                               k=5,
                               zoom_start=13,
                               scheme='equalinterval',
                               legend_kwds=dict(colorbar=False, fmt='{:.0f}'),
                               legend=True,
                               tooltip=['nama_desa', 'id_desa', 'population'],
                               cmap='Blues_r')
    gdf_catch.boundary.explore(m=m,
                               color='red',
                               style_kwds=dict(weight=5),
                               legend=False)
    geo_df_list = [[point.xy[1][0], point.xy[0][0]]
                   for point in gdf_loc.geometry]
    for i, coordinates in enumerate(geo_df_list):
        folium.Marker(
            location=coordinates,
            icon=folium.Icon(color="darkblue", icon_color='#FDD212',
                             icon="fa-university", prefix='fa'),
            popup="Location : " + str(gdf_catch.reset_index()['id'][i])
        ).add_to(m)
    return m


def demog_map_per_desa(gdf_demog, gdf_catch, gdf_loc, id_desa):
    color1 = '#0D2C5B'
    color2 = '#FDD212'
    desa = gdf_demog[gdf_demog['id_desa'] == id_desa].reset_index()
    gdf_demog_join = gpd.sjoin(gdf_demog, gdf_catch[['geometry', 'id']])
    m = gdf_demog_join.explore(tiles='Cartodb Positron',
                               legend=False,
                               zoom_start=13,
                               style_kwds=dict(color='gray', opacity=0.4))
    desa.explore(
        m=m,
        color=color1
    )
    gdf_catch.boundary.explore(
        m=m,
        color='red',
        style_kwds=dict(weight=5)
    )

    import folium
    geo_df_list = [[point.xy[1][0], point.xy[0][0]]
                   for point in gdf_loc.geometry]
    for i, coordinates in enumerate(geo_df_list):
        folium.Marker(
            location=coordinates,
            icon=folium.Icon(color="darkblue", icon_color='#FDD212',
                             icon="fa-university", prefix='fa'),
            popup="Location : " + str(gdf_catch.reset_index()['id'][i])
        ).add_to(m)

    return m


def demog_map_all(gdf_demog, gdf_catch, gdf_loc):
    color1 = '#0D2C5B'
    color2 = '#FDD212'
    gdf_demog_join = gpd.sjoin(gdf_demog, gdf_catch[['geometry', 'id']])
    m = gdf_demog_join.explore(tiles='Cartodb Positron',
                               legend=False,
                               zoom_start=13,
                               style_kwds=dict(color='gray', opacity=0.4),
                               name='Admin Layer')
    for id_desa in gdf_demog.id_desa.unique().tolist():
        desa = gdf_demog[gdf_demog['id_desa'] == id_desa].reset_index()
        nama_desa = desa.nama_desa[0]
        desa.explore(m=m,
                     color=color1,
                     name=str(nama_desa))

    gdf_catch.boundary.explore(
        m=m,
        color='red',
        style_kwds=dict(weight=5),
        name='Catchment Area'
    )
    folium.LayerControl().add_to(m)
    geo_df_list = [[point.xy[1][0], point.xy[0][0]]
                   for point in gdf_loc.geometry]
    for i, coordinates in enumerate(geo_df_list):
        folium.Marker(
            location=coordinates,
            icon=folium.Icon(color="darkblue", icon_color='#FDD212',
                             icon="fa-university", prefix='fa'),
            popup="Location : " + str(gdf_catch.reset_index()['id'][i])
        ).add_to(m)

    return m


def demog_chart_spesific(gdf_demog, gdf_catch, variable, proj='epsg:3395'):
    color1 = '#325285'
    color2 = '#FDD212'
    color = get_color_gradient(color1, color2, 6)

    # calculate percentage of demog in catchment
    gdf_demog_join = gpd.sjoin(gdf_demog, gdf_catch[['id', 'geometry']])
    for nama_id in gdf_demog_join.id.unique().tolist():
        percentage = pd.DataFrame()
        percentage['kode_desa'] = []
        percentage['percent'] = []
        x = gpd.clip(gdf_demog_join, gdf_catch).reset_index()
        y = gdf_demog_join
        percentage['kode_desa'] = x.kode_desa.unique()
        percentage['percent'] = x.to_crs(
            proj).area/gdf_catch.to_crs(proj).area[0]

        percentage['kode_desa'] = percentage['kode_desa'].astype(str)
        demog_percent = pd.merge(percentage, gdf_demog_join.drop(columns=['id_desa', 'nama_desa',
                                                                          'id_kota', 'nama_kota', 'geometry']), on='kode_desa')
        demog_i = gdf_demog_join[gdf_demog_join['id'] == nama_id].reset_index()
        demog_cal = demog_i[['kode_desa', 'geometry']].copy()

        columns = demog_percent.columns.tolist()
        variable = variable
        var = []
        not_var = []
        for i in variable:
            if i in columns:
                var.append(i)
            else:
                not_var.append(i)

        for i in var:
            demog_cal[i] = round(demog_percent['percent']*demog_percent[i])

        list_male = ['LK_15_19', 'LK_20_24', 'LK_25_29', 'LK_30_34',
                     'LK_35_39', 'LK_40_44', 'LK_45_49', 'LK_50_54', 'LK_55_59']
        list_female = ['PR_15_19', 'PR_20_24', 'PR_25_29', 'PR_30_34',
                       'PR_35_39', 'PR_40_44', 'PR_45_49', 'PR_50_54', 'PR_55_59']
        male = pd.DataFrame(demog_cal[list_male].sum(axis=0)).reset_index()
        male.columns = ['index', 'male']
        female = pd.DataFrame(demog_cal[list_female].sum(axis=0)).reset_index()
        female.columns = ['index', 'female']
        ages = pd.DataFrame({'keterangan': ['Ages 15-19',
                                            'Ages 20-24',
                                            'Ages 25-29',
                                            'Ages 30-34',
                                            'Ages 35-39',
                                            'Ages 40-44',
                                            'Ages 45-49',
                                            'Ages 50-54',
                                            'Ages 55-59',
                                            ]})
        a = pd.concat([ages, male['male']], axis=1)
        df_ages = pd.concat([a, female['female']], axis=1)
        y_age = df_ages['keterangan']
        x_M = df_ages['male']
        x_F = df_ages['female'] * -1

        color1 = '#325285'
        color2 = '#FDD212'

        fig = go.Figure()

        # Adding Male data to the figure
        fig.add_trace(go.Bar(y=y_age, x=x_M,
                             name='Male',
                             orientation='h', marker_color=color1))

        # Adding Female data to the figure
        fig.add_trace(go.Bar(y=y_age, x=x_F,
                             name='Female', orientation='h', marker_color=color2))
        bt1 = round(
            demog_cal[list_male+list_female].sum(axis=0).max()/1000)*1000
        bt2 = round(
            demog_cal[list_male+list_female].sum(axis=0).max()/1000)*1000/2
        # Updating the layout for our graph
        fig.update_layout(height=500, title='Population Pyramid based on Gender in Catchment '+nama_id,
                          title_font_size=16, barmode='relative',
                          bargap=0.0, bargroupgap=0,
                          xaxis=dict(tickvals=[-1*bt1, -1*bt2, 0,
                                               bt2, bt1],

                                     title='Population in Millions',
                                     title_font_size=12)
                          )

        return fig


def demog_chart_perdesa(gdf_demog,  id_desa):
    color1 = '#325285'
    color2 = '#FDD212'

    list_male = ['LK_15_19', 'LK_20_24', 'LK_25_29', 'LK_30_34',
                 'LK_35_39', 'LK_40_44', 'LK_45_49', 'LK_50_54', 'LK_55_59']
    list_female = ['PR_15_19', 'PR_20_24', 'PR_25_29', 'PR_30_34',
                   'PR_35_39', 'PR_40_44', 'PR_45_49', 'PR_50_54', 'PR_55_59']
    data = gdf_demog[gdf_demog['id_desa'] == id_desa].reset_index()
    male = data[list_male].T.reset_index()
    male.columns = ['index', 'male']
    female = data[list_female].T.reset_index()
    female.columns = ['index', 'female']
    ages = pd.DataFrame({'keterangan': ['Ages 15-19',
                                        'Ages 20-24',
                                        'Ages 25-29',
                                        'Ages 30-34',
                                        'Ages 35-39',
                                        'Ages 40-44',
                                        'Ages 45-49',
                                        'Ages 50-54',
                                        'Ages 55-59',
                                        ]})
    a = pd.concat([ages, male['male']], axis=1)
    df_ages = pd.concat([a, female['female']], axis=1)
    y_age = df_ages['keterangan']
    x_M = df_ages['male']
    x_F = df_ages['female'] * -1

    bt1 = round(data[list_male+list_female].sum(axis=0).max()/1000)*1000
    bt2 = round(data[list_male+list_female].sum(axis=0).max()/1000)*1000/2
    fig = go.Figure()

    # Adding Male data to the figure
    fig.add_trace(go.Bar(y=y_age, x=x_M,
                         name='Male',
                         orientation='h', marker_color=color1))

    # Adding Female data to the figure
    fig.add_trace(go.Bar(y=y_age, x=x_F,
                         name='Female', orientation='h', marker_color=color2))

    # Updating the layout for our graph
    fig.update_layout(height=500, title='Population Pyramid based on Gender in {}'.format(data.nama_desa[0]),
                      title_font_size=22, barmode='relative',
                      bargap=0.0, bargroupgap=0,
                      xaxis=dict(tickvals=[-1*bt1, -1*bt2, 0,
                                           bt2, bt1],

                                 title='Population',
                                 title_font_size=14)
                      )
    return fig


def demog_chart_all(gdf_demog, gdf_catch, variable, proj='epsg:3395'):
    # calculate percentage of demog in catchment
    for nama_id in gdf_catch.id.unique().tolist():
        catch = gdf_catch[gdf_catch['id'] == nama_id].reset_index()
        gdf_demog_join = gpd.sjoin(gdf_demog, catch[['id', 'geometry']])
        percentage = pd.DataFrame()
        percentage['kode_desa'] = []
        percentage['percent'] = []
        x = gpd.clip(gdf_demog_join, catch).reset_index()
        y = gdf_demog_join
        percentage['kode_desa'] = x.kode_desa.unique()
        percentage['percent'] = x.to_crs(proj).area/catch.to_crs(proj).area[0]

        percentage['kode_desa'] = percentage['kode_desa'].astype(str)
        demog_percent = pd.merge(percentage, gdf_demog_join.drop(columns=['id_desa', 'nama_desa',
                                                                          'id_kota', 'nama_kota', 'geometry']), on='kode_desa')
        demog_i = gdf_demog_join[gdf_demog_join['id'] == nama_id].reset_index()
        demog_cal = demog_i[['kode_desa', 'geometry']].copy()

        columns = demog_percent.columns.tolist()
        variable = variable
        var = []
        not_var = []
        for i in variable:
            if i in columns:
                var.append(i)
            else:
                not_var.append(i)

        for i in var:
            demog_cal[i] = round(demog_percent['percent']*demog_percent[i])

        list_male = ['LK_15_19', 'LK_20_24', 'LK_25_29', 'LK_30_34',
                     'LK_35_39', 'LK_40_44', 'LK_45_49', 'LK_50_54', 'LK_55_59']
        list_female = ['PR_15_19', 'PR_20_24', 'PR_25_29', 'PR_30_34',
                       'PR_35_39', 'PR_40_44', 'PR_45_49', 'PR_50_54', 'PR_55_59']
        male = pd.DataFrame(demog_cal[list_male].sum(axis=0)).reset_index()
        male.columns = ['index', 'male']
        female = pd.DataFrame(demog_cal[list_female].sum(axis=0)).reset_index()
        female.columns = ['index', 'female']
        ages = pd.DataFrame({'keterangan': ['Ages 15-19',
                                            'Ages 20-24',
                                            'Ages 25-29',
                                            'Ages 30-34',
                                            'Ages 35-39',
                                            'Ages 40-44',
                                            'Ages 45-49',
                                            'Ages 50-54',
                                            'Ages 55-59',
                                            ]})
        a = pd.concat([ages, male['male']], axis=1)
        df_ages = pd.concat([a, female['female']], axis=1)
        y_age = df_ages['keterangan']
        x_M = df_ages['male']
        x_F = df_ages['female'] * -1

        color1 = '#325285'
        color2 = '#FDD212'

        fig = go.Figure()

        # Adding Male data to the figure
        fig.add_trace(go.Bar(y=y_age, x=x_M,
                             name='Male',
                             orientation='h', marker_color=color1))

        # Adding Female data to the figure
        fig.add_trace(go.Bar(y=y_age, x=x_F,
                             name='Female', orientation='h', marker_color=color2))
        bt1 = round(gdf_demog_join[list_male +
                    list_female].sum(axis=1).max()/1000)*1000
        bt2 = round(gdf_demog_join[list_male +
                    list_female].sum(axis=1).max()/1000)*1000/2
        fig.update_layout(height=500, title='Population Pyramid based on Gender in Catchment '+nama_id,
                          title_font_size=16, barmode='relative',
                          bargap=0.0, bargroupgap=0,
                          xaxis=dict(tickvals=[-1*bt1, -1*bt2, 0,
                                               bt2, bt1],

                                     title='Population',
                                     title_font_size=12)
                          )
        # Updating the layout for our graph
        for id_desa in gdf_demog_join.id_desa.unique().tolist():
            data = gdf_demog[gdf_demog['id_desa'] == id_desa].reset_index()
            male = data[list_male].T.reset_index()
            male.columns = ['index', 'male']
            female = data[list_female].T.reset_index()
            female.columns = ['index', 'female']
            ages = pd.DataFrame({'keterangan': ['Ages 15-19',
                                                'Ages 20-24',
                                                'Ages 25-29',
                                                'Ages 30-34',
                                                'Ages 35-39',
                                                'Ages 40-44',
                                                'Ages 45-49',
                                                'Ages 50-54',
                                                'Ages 55-59',
                                                ]})
            a = pd.concat([ages, male['male']], axis=1)
            df_ages = pd.concat([a, female['female']], axis=1)
            y_age = df_ages['keterangan']
            x_M = df_ages['male']
            x_F = df_ages['female'] * -1

            bt1 = round(
                data[list_male+list_female].sum(axis=0).max()/1000)*1000
            bt2 = round(
                data[list_male+list_female].sum(axis=0).max()/1000)*1000/2

            # Adding Male data to the figure
            fig.add_trace(go.Bar(y=y_age, x=x_M,
                                 name='Male',
                                 orientation='h', marker_color=color1))

            # Adding Female data to the figure
            fig.add_trace(go.Bar(y=y_age, x=x_F,
                                 name='Female', orientation='h', marker_color=color2))
            bt1 = round(
                data[list_male+list_female].sum(axis=1).max()/1000)*1000
            bt2 = round(
                data[list_male+list_female].sum(axis=1).max()/1000)*1000/2
            fig.update_layout(xaxis=dict(tickvals=[-1*bt1, -1*bt2, 0,
                                                   bt2, bt1],

                                         title='Population',
                                         title_font_size=12)
                              )
            # Updating the layout for our graph
        list_visible = []
        for i in range(0, gdf_demog_join.id_desa.nunique()+1):
            a = [True]*2
            b = [False]
            visible_false = b*(gdf_demog_join.id_desa.nunique()+1)*2
            visible_false[i*2:i*2+2] = a
            list_visible.append(visible_false)

        first = ['CATCHMENT']
        second = gdf_demog_join.nama_desa.tolist()
        data = first+second

        fig.update_layout(
            updatemenus=[
                dict(
                    active=0,
                    buttons=list([
                                 dict(label=id_desa,
                                      method="update",
                                      args=[{"visible": list_visible[index]},
                                            {"title": "Population Pyramid in {}, {}".format(nama_id, id_desa)}]) for index, id_desa in enumerate(data)
                                 ]
                                 ))
            ])

        return fig


def mw_chart_timeseries(gdf_catch, grid, mw):
    color1 = '#325285'
    color2 = '#FDD212'

    mw['Hour'] = mw['time'].dt.hour
    mw['Date'] = mw['time'].dt.date
    mw['weekday'] = mw['time'].dt.weekday
    mw['WeekDay'] = np.where(mw['weekday'] == 0, 'Monday',
                             np.where(mw['weekday'] == 1, 'Tuesday',
                                      np.where(mw['weekday'] == 2, 'Wednesday',
                                               np.where(mw['weekday'] == 3, 'Thursday',
                                                        np.where(mw['weekday'] == 4, 'Friday',
                                                                 np.where(mw['weekday'] == 5, 'Saturday', 'Sunday'))))))
    mw['Date'] = mw['Date'].astype('str')

    mw['Segment'] = np.where(mw['Hour'].isin([1, 2, 3, 4, 5, 6]), '0 - 6',
                             np.where(mw['Hour'].isin([7, 8, 9, 10, 11, 12]), '7 - 12',
                                      np.where(mw['Hour'].isin([13, 14, 15, 16, 17, 18]), '13 - 18',
                                               '19 - 24')))
    grid_join = gpd.sjoin(grid, gdf_catch[['id', 'geometry']]).drop(
        columns='index_right')
    mw_merge = pd.merge(mw, grid_join[['gid', 'id']])
    # Date
    for j in mw_merge.id.unique():
        telco = mw_merge[mw_merge['id'] == j]
        group = telco.groupby('Date')['counts'].sum().reset_index()
        fig = px.line(group,
                      x='Date',
                      y='counts',
                      title="Telco Data Timeseries by Date, "+'<b>'+j+'</b>',
                      markers=True,
                      height=500
                      )
        fig.update_traces(line_color=color1)
        fig.update_layout(xaxis_title='Date',
                          yaxis_title="Total Population")
    return fig


def mw_chart_hours(gdf_catch, grid, mw):
    color1 = '#325285'
    color2 = '#FDD212'

    mw['Hour'] = mw['time'].dt.hour
    mw['Date'] = mw['time'].dt.date
    mw['weekday'] = mw['time'].dt.weekday
    mw['WeekDay'] = np.where(mw['weekday'] == 0, 'Monday',
                             np.where(mw['weekday'] == 1, 'Tuesday',
                                      np.where(mw['weekday'] == 2, 'Wednesday',
                                               np.where(mw['weekday'] == 3, 'Thursday',
                                                        np.where(mw['weekday'] == 4, 'Friday',
                                                                 np.where(mw['weekday'] == 5, 'Saturday', 'Sunday'))))))
    mw['Date'] = mw['Date'].astype('str')

    mw['Segment'] = np.where(mw['Hour'].isin([1, 2, 3, 4, 5, 6]), '0 - 6',
                             np.where(mw['Hour'].isin([7, 8, 9, 10, 11, 12]), '7 - 12',
                                      np.where(mw['Hour'].isin([13, 14, 15, 16, 17, 18]), '13 - 18',
                                               '19 - 24')))
    grid_join = gpd.sjoin(grid, gdf_catch[['id', 'geometry']]).drop(
        columns='index_right')
    mw_merge = pd.merge(mw, grid_join[['gid', 'id']])

    # Hour
    for j in mw_merge.id.unique():
        telco = mw_merge[mw_merge['id'] == j].reset_index()
        hour = np.arange(0, 24, dtype=int)
        telco['Hour'] = telco['Hour'].astype('str')
        fig = px.box(telco,
                     height=500,
                     x='Hour',
                     y='counts',
                     title="Telco Data Timeseries by Hours, "+'<b>'+j+'</b>')
        fig.update_xaxes(categoryorder='array',
                         categoryarray=[str(x) for x in hour])
        fig.update_traces(marker_color=color1,
                          marker_line_color=color2,
                          marker_line_width=0.4)
        fig.update_layout(xaxis_title='Hours',
                          yaxis_title="Total Population")
    return fig


def mw_chart_weekdays(gdf_catch, grid, mw):
    color1 = '#325285'
    color2 = '#FDD212'

    mw['Hour'] = mw['time'].dt.hour
    mw['Date'] = mw['time'].dt.date
    mw['weekday'] = mw['time'].dt.weekday
    mw['WeekDay'] = np.where(mw['weekday'] == 0, 'Monday',
                             np.where(mw['weekday'] == 1, 'Tuesday',
                                      np.where(mw['weekday'] == 2, 'Wednesday',
                                               np.where(mw['weekday'] == 3, 'Thursday',
                                                        np.where(mw['weekday'] == 4, 'Friday',
                                                                 np.where(mw['weekday'] == 5, 'Saturday', 'Sunday'))))))
    mw['Date'] = mw['Date'].astype('str')

    mw['Segment'] = np.where(mw['Hour'].isin([1, 2, 3, 4, 5, 6]), '0 - 6',
                             np.where(mw['Hour'].isin([7, 8, 9, 10, 11, 12]), '7 - 12',
                                      np.where(mw['Hour'].isin([13, 14, 15, 16, 17, 18]), '13 - 18',
                                               '19 - 24')))
    grid_join = gpd.sjoin(grid, gdf_catch[['id', 'geometry']]).drop(
        columns='index_right')
    mw_merge = pd.merge(mw, grid_join[['gid', 'id']])

    # Weekdays
    for j in mw_merge.id.unique():
        telco = mw_merge[mw_merge['id'] == j].reset_index()
        hour = ['Monday', 'Tuesday', 'Wednesday',
                'Thursday', 'Friday', 'Saturday', 'Sunday']
        telco['WeekDay'] = telco['WeekDay'].astype('str')
        fig = px.box(telco,
                     height=500,
                     x='WeekDay',
                     y='counts',
                     title="Telco Data Timeseries by Weekdays, "+'<b>'+j+'</b>')
        fig.update_xaxes(categoryorder='array',
                         categoryarray=[str(x) for x in hour])
        fig.update_traces(marker_color=color1,
                          marker_line_color=color2,
                          marker_line_width=0.4)
        fig.update_layout(xaxis_title='WeekDays',
                          yaxis_title="Total Population")
    return fig


def mw_chart_segmenttime(gdf_catch, grid, mw):
    color1 = '#325285'
    color2 = '#FDD212'

    mw['Hour'] = mw['time'].dt.hour
    mw['Date'] = mw['time'].dt.date
    mw['weekday'] = mw['time'].dt.weekday
    mw['WeekDay'] = np.where(mw['weekday'] == 0, 'Monday',
                             np.where(mw['weekday'] == 1, 'Tuesday',
                                      np.where(mw['weekday'] == 2, 'Wednesday',
                                               np.where(mw['weekday'] == 3, 'Thursday',
                                                        np.where(mw['weekday'] == 4, 'Friday',
                                                                 np.where(mw['weekday'] == 5, 'Saturday', 'Sunday'))))))
    mw['Date'] = mw['Date'].astype('str')

    mw['Segment'] = np.where(mw['Hour'].isin([1, 2, 3, 4, 5, 6]), '0 - 6',
                             np.where(mw['Hour'].isin([7, 8, 9, 10, 11, 12]), '7 - 12',
                                      np.where(mw['Hour'].isin([13, 14, 15, 16, 17, 18]), '13 - 18',
                                               '19 - 24')))
    grid_join = gpd.sjoin(grid, gdf_catch[['id', 'geometry']]).drop(
        columns='index_right')
    mw_merge = pd.merge(mw, grid_join[['gid', 'id']])

    # Segment Hour
    for j in mw_merge.id.unique():
        telco = mw_merge[mw_merge['id'] == j].reset_index()
        group = telco.groupby(['Date', 'Segment'])[
            'counts'].sum().reset_index()
        group2 = group.groupby('Segment')['counts'].mean().reset_index()
        group2['counts'] = round(group2['counts'])
        fig = px.bar(group2, x="Segment", y="counts",
                     color='Segment', text='counts',
                     title='Telco Data segmentation by Time, '+'<b>'+j+'</b>',
                     height=500,
                     category_orders={'Segment': ['0 - 6', '7 - 12', '13 - 18', '19 - 24']})
        fig.update_traces(marker_color=color1,
                          marker_line_color='white',
                          marker_line_width=3, )
        fig.update_layout(xaxis_title="Hours",
                          yaxis_title="Average Population")
    return fig


def mw_chart_heatmap(gdf_catch, grid,  mw):
    color1 = '#325285'
    color2 = '#FDD212'

    mw['Hour'] = mw['time'].dt.hour
    mw['Date'] = mw['time'].dt.date
    mw['weekday'] = mw['time'].dt.weekday
    mw['WeekDay'] = np.where(mw['weekday'] == 0, 'Monday',
                             np.where(mw['weekday'] == 1, 'Tuesday',
                                      np.where(mw['weekday'] == 2, 'Wednesday',
                                               np.where(mw['weekday'] == 3, 'Thursday',
                                                        np.where(mw['weekday'] == 4, 'Friday',
                                                                 np.where(mw['weekday'] == 5, 'Saturday', 'Sunday'))))))
    mw['Date'] = mw['Date'].astype('str')

    mw['Segment'] = np.where(mw['Hour'].isin([1, 2, 3, 4, 5, 6]), '0 - 6',
                             np.where(mw['Hour'].isin([7, 8, 9, 10, 11, 12]), '7 - 12',
                                      np.where(mw['Hour'].isin([13, 14, 15, 16, 17, 18]), '13 - 18',
                                               '19 - 24')))
    grid_join = gpd.sjoin(grid, gdf_catch[['id', 'geometry']]).drop(
        columns='index_right')
    mw_merge = pd.merge(mw, grid_join[['gid', 'id']])

    # Heatmap by days and Hour
    for j in mw_merge.id.unique():
        telco = mw_merge[mw_merge['id'] == j].reset_index()

        telco['Days'] = telco['time'].dt.day
        group = telco.groupby(['Date', 'Days', 'Hour'])[
            'counts'].sum().reset_index()
        group2 = group.groupby(['Days', 'Hour'])['counts'].mean().reset_index()
        group2['counts'] = round(group2['counts'])
        list_test = []
        for i in np.arange(1, 32, dtype=int):
            test = group2[group2['Days'] == i].reset_index()
            test['count'] = test['counts']/test['counts'].sum()*100
            list_test.append(test)

        list_z = []
        group_by = pd.concat(list_test).drop(columns='index')
        for i in np.arange(0, 24, dtype=int):
            data = group_by[(group_by['Hour'] == i)]
            listed = data.sort_values('Days')['count'].tolist()
            list_z.append(listed)
        z = np.array(list_z)
        day = np.arange(1, 32, dtype=int)
        fig = px.imshow(z,
                        text_auto=".2f",
                        color_continuous_scale='Blues',
                        aspect="auto",
                        height=800,
                        width=1200,
                        title='Telco Data Heatmap, '+'<b>'+j+'</b>',
                        )
        fig.update_layout(
            xaxis_nticks=36,
            yaxis_nticks=36,
            xaxis_title="Days",
            yaxis_title="Hours",
            font=dict(
                size=9))
        fig.update_yaxes(autorange="reversed")
    return fig


def poi_map(gdf_poi, catch_poly, df_loc, classify='group_name'):
    top10 = gdf_poi.groupby(classify)['geometry'].count().reset_index().sort_values(
        'geometry', ascending=False)[:10][classify].tolist()
    poi_clip = gpd.clip(gdf_poi, catch_poly[['geometry']])
    poi1 = poi_clip[poi_clip[classify].isin(top10)].reset_index()
    poi2 = poi_clip[~poi_clip[classify].isin(top10)].reset_index()
    poi2[classify] = 'Others'
    poi_plot = pd.concat([poi1, poi2])
    # map visualization
    poi_clip = gpd.clip(gdf_poi, catch_poly[['geometry']])

    m = catch_poly.explore(
        tiles='Cartodb Positron',
        color='grey',
        zoom_start=14,
    )
    if classify == 'group_name':
        poi_plot.explore(
            m=m,
            column=classify,
            legend_kwds=dict(colorbar=False, fmt='{:.0f}'),
            legend=True,
            categories=top10+['Others'],
            cmap='Paired',
        )
    else:
        poi_plot.explore(
            m=m,
            column=classify,
            legend_kwds=dict(colorbar=False, fmt='{:.0f}'),
            legend=True,
            categories=top10,
            cmap='OrRd'
        )
    geo_df_list = [[point.xy[1][0], point.xy[0][0]]
                   for point in df_loc.geometry]
    for i, coordinates in enumerate(geo_df_list):
        folium.Marker(
            location=coordinates,
            icon=folium.Icon(color="darkblue", icon_color='#FDD212',
                             icon="fa-university", prefix='fa'),
            popup="Location : " + str(catch_poly.reset_index()['id'][i])
        ).add_to(m)
    return m


def poi_chart(gdf_poi, catch_poly):
    color1 = '#0D2C5B'
    color2 = '#FDD212'
    color3 = '#f1f2ce'

    color = get_color_gradient(color1, color2, gdf_poi.group_name.nunique())
    gdf_join = gpd.sjoin(gdf_poi, catch_poly[['geometry', 'id']])
    for j in gdf_join.id.unique():
        gdf_poi_join = gdf_join[gdf_join['id'] == j].reset_index()
        catch = catch_poly[catch_poly['id'] == j].reset_index()
        group = gdf_poi_join.groupby('group_name')[
            'geometry'].count().reset_index()
        fig = px.bar(group.sort_values('geometry'),
                     y='group_name',
                     x='geometry',
                     text_auto=True,
                     title="Total POI in Catchment based on Category, "+'<b>'+j+'</b>',
                     orientation='h',
                     height=700
                     )

        fig.update_xaxes(categoryorder='array',
                         categoryarray=group.sort_values('geometry', ascending=False)['group_name'].tolist())
        fig.update_traces(marker_color=color1,
                          marker_line_color=color1,
                          marker_line_width=1.5)
        fig.update_layout(yaxis_title="Category",
                          xaxis_title="Total POI")
        return fig
    

def pie_chart(df_poi_atm):

    df_group=df_poi_atm.groupby(['keterangan']).size().reset_index(name='count')
    color1 = '#325285'
    color2 = '#FDD212'
    fig = px.pie(df_group, values='count', names='keterangan',color='keterangan', 
                color_discrete_map={
                    'Competitor': color2,
                'Mandiri': color1},  title='Customer',
                height=500, width=400)
    fig.update_layout(title_x=0.3)

    return fig
