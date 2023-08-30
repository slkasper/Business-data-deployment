import geopandas as gpd
import pydeck as pdk
from pydeck.types import String
from shapely import wkt
import streamlit as st


import data_science_utils as dsu

import src

white = [255,255,255]   #for get_line_color on dark map
black = [0,0,0]         #for get_line_color on a light map

def find_center(df):
    return df['latitude'].mean(), df['longitude'].mean()

def color_map() -> dict:
    '''Define color mapping for segments'''
    return {
        'microenterprise':         [255, 255,   0],   # Yellow   
        'small_business':          [255, 191,   0],   # Orange
        'small_medium_enterprise': [255, 129,  19],   # Red-Orange
        'large_enterprise':        [255,   0,   0]    # Red
    }

@st.cache_data
def add_color(df):
    '''Apply color based on segments'''
    cmap = color_map()
    df['color'] = df['segment'].map(cmap)
    return df

@st.cache_data
def create_scatter_layer(df):
    '''Create Scatterplot layer with color mapping'''
    scatterplot = pdk.Layer(
        'ScatterplotLayer',
        data=df,
        get_position='[longitude, latitude]',
        get_radius=20,
        get_color='color',
        pickable=True,
        opacity=0.2,
        stroked=True,
        filled=True,
        radius_scale=10,
        line_width_min_pixels=1,
        get_line_color=[0, 0, 0],
    )
    return scatterplot

def create_gdf(df, geometry_column):
    '''
    Takes a df with a ST_AsText() column and converts that column into a column of crs values.
    Renames the column to df['geometry'] and converts the df to a geopandasDF
    Outputs the geoDF with the new 'geometry' column.
    '''
    # Convert geometry to wkt 
    df[geometry_column] = df[geometry_column].apply(lambda x: wkt.loads(x))
    crs="EPSG:4326"
    # Convert to gdf, set crs, and de-dupe geom column
    df = gpd.GeoDataFrame(df, geometry=df[geometry_column])
    df = df.set_crs(crs)
    df = df.drop(geometry_column, axis=1)
    return df 

def create_polygon_df(df):
    # Convert the dataframe to a geodataframe using the 'shape' column
    cab_df = create_gdf(df, "shape")

    # Reduce columns to 'name' and 'geometry'
    cab_df = df[['cabinet_name', 'latitude', 'longitude', 'geometry']].drop_duplicates()

    # Add a boundary column by using convert_geom_to_coord function on lambda, applying the func to each row val
    cab_df['boundary'] = cab_df['geometry'].apply(lambda x: dsu.convert_geom_to_coord_list(x))
    
    # PolygonLayer needs the dataframe to ONLY have boundary column. Get obj errors otherwise:
    #   TypeError: vars() argument must have __dict__ attribute
    polygon_df = cab_df[['boundary']]
    return polygon_df


@st.cache_data
def create_cab_boundary_layer(polygon_df):
    cab_bound_layer = pdk.Layer(
            "PolygonLayer",
            polygon_df,
            stroked=True,
            get_polygon="boundary",
            filled=False,
            extruded=False,
            wireframe=False,
            get_elevation=0,
            get_line_width=50,
            get_line_color= white,
            auto_highlight=True,
            pickable=False,

	    )
    return cab_bound_layer


def create_cab_text_df(df):
    df["centroid"] = df["geometry"].apply(lambda row: [row.centroid.x, row.centroid.y])
    text_df = df[['cabinet_name','centroid']]
    return text_df
    
@st.cache_data
def create_cab_labels(text_df):

    text_layer = pdk.Layer(
        "TextLayer",
        text_df,
        pickable=False,
        get_position="centroid",
        get_text="cabinet_name",
        get_size=72,
        get_color=white,
        get_angle=0,
        font_family="Arial, sans-serif",
        # Note that string constants in pydeck are explicitly passed as strings
        # This distinguishes them from columns in a data set
        get_text_anchor=String("middle"),
        get_alignment_baseline=String("center"),
        )
    return text_layer
    
#this should be adjusted to add any layers you need
def build_layers(scatterplot):
    '''Input all the layers you need, output a list of layers for PyDeck View'''
    layers = [scatterplot]
    return layers

def create_view(df, layers:list):
    '''Create PyDeck view'''
    init_latitude, init_longitude = find_center(df)
    view_state = pdk.ViewState(latitude=init_latitude, longitude=init_longitude, zoom=10)
    # scatterplot = create_scatter_layer(df)
    # cab_boundary = create_cab_boundary_layer(df)
    # cab_labels = create_cab_labels(df)
    
    # if subdivisions:
    #     layers = [scatterplot, cab_boundary, cab_labels]
    # else:
    #     layers = [scatterplot]
    r = pdk.Deck(layers, initial_view_state=view_state, 
                tooltip={"text": "{company_name}\n{location_address}\n{segment}\n{name}"}) # type: ignore
    return r
