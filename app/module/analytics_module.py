import geopandas as gpd
import pandas as pd


def gdf_loc(longitude, latitude, id_point):
    """
    func untuk membuat geodataframe dari setiap titik mandiri
    """

    # create dataframe
    df = pd.DataFrame({'id': [id_point],
                       'lon': [longitude],
                       'lat': [latitude]})
    gdf = gpd.GeoDataFrame(df, geometry=gpd.points_from_xy(
        df.lon, df.lat), crs='epsg:4326')

    return gdf


def catchment(gdf_loc, dt, proj='epsg:3395'):
    """
    func digunakan untuk membuat catchment area berupa buffer
    """
    # buffering
    buffer = gpd.GeoDataFrame(gdf_loc.to_crs(proj).buffer(dt))
    buffer.columns = ['geometry']
    buffer.crs = proj
    buffer['id'] = gdf_loc['id']
    buffer = buffer.to_crs('epsg:4326')

    return buffer
