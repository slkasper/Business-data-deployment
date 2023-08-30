import data_science_utils as dsu
import streamlit as st
from dotenv import load_dotenv 

load_dotenv() # TODO: move to dsu package

#Test the connection
conn = dsu.create_redshift_connection()

#CREATE INDEX [indexname] ON [tablename] USING GIST ( [geometryfield] ); 

@st.cache_data
def load_business_data():
    """
    Get Segment data from cur_data_axle.business_data. 
    WHERE clause filters out bad data and sets up cabinets
    """
    query = '''
        SELECT 
             --{#- business_data_axle -#}
            company_name, location_address, location_city, 
            location_state, loc_sales_vol_int,
            dab.latitude as latitude,
            dab.longitude as longitude,
            geometry, segment, naics,
            naics_description,
            left(naics,2) as naics_cat,
            location_employee_size_range,
            telcom_expenses
            
            --{#- community_subdivisions -#}
            , type
            , ST_AsText(shape) as shape
            , cs.name as cabinet_name
        FROM cur_data_axle.business_data as dab
        JOIN  cur_community.subdivisions as cs
        ON ST_Contains(cs.shape, dab.geometry)
        WHERE type = 'cabinet'
        AND company_name NOT in ('Ecannplus', 'Payne I P Law', 
            'Sisters Of St Francis', '360 Tour Designs')
        ORDER BY loc_sales_vol_int desc
    '''
    # return create_df(query)
    return dsu.run_query(query)


@st.cache_data
def load_cabinets():
    '''
    Load cabinet locations from community subdivisions
    '''
    query = '''
        SELECT name, latitude, longitude 
        , shape
        FROM cur_community.subdivisions 
        WHERE type = 'cabinet'
    '''
    # return create_df(query)
    return dsu.run_query(query)

def create_df(query):
    '''
    Creates pandas dataframe from redshift query string
    '''
    with conn.cursor() as cursor:
        cursor.execute(query)
        df = cursor.fetch_dataframe()
    return df

# TODO --
# @st.cache_data
# def main():
#     cabinets = load_cabinets()
#     data = load_data()
#     # add color the data here
#     return cabinets, data

# cabinets, df = main()