# import data_science_utils as dsu
import os
import snowflake.connector
import streamlit as st
from dotenv import load_dotenv 

load_dotenv() # TODO: move to dsu package

PASSWORD = os.getenv('SNOWSQL_PWD')
WAREHOUSE = os.getenv('WAREHOUSE')

ctx = snowflake.connector.connect(
    user='SonyaK',
    password=PASSWORD,
    account='myorganization-myaccount',
    )

# #Test the connection
# conn = dsu.create_redshift_connection()

@st.cache_data
def load_business_data():
    """
    Get Segment data from cur_data_axle.business_data. 
    WHERE clause filters out bad data and sets up cabinets
    """
    query = '''
    SELECT 
        --{#- business_data_axle -#}
        name, address,
        city,
        state, locamount, --loc_sales_vol_int,
        lat as latitude,
        lon as longitude,
        PRIMNAICSCODE as naics,
        PRIMNAICSDESC as naics_desc,
        left(PRIMNAICSCODE,2) as naics_cat
        --- location_employee_size_range,
        --- telcom_expenses
    FROM cur_data_axle.business_data
    ---WHERE company_name NOT in ('Ecannplus', 'Payne I P Law', 
    ---'Sisters Of St Francis', '360 Tour Designs')   

    '''
    return create_df(query)
    # return dsu.run_query(query)

        # WHERE type = 'cabinet'
        # AND company_name NOT in ('Ecannplus', 'Payne I P Law', 
        #     'Sisters Of St Francis', '360 Tour Designs')

# @st.cache_data
# def load_cabinets():
#     '''
#     Load cabinet locations from community subdivisions
#     '''
#     query = '''
#         SELECT 
#              --{#- business_data_axle -#}
#             dab.latitude as latitude,
#             dab.longitude as longitude,
#             geometry
            
#             --{#- community_subdivisions -#}
#             , type
#             , ST_AsText(shape) as shape
#             , cs.name 
#             , CONCAT('Cabinet ', LPAD(SUBSTRING(cs.name, 9), 2, '0')) AS name
#             , SPLIT_PART(name, ' ', 2) as cabinet_name
#         FROM cur_data_axle.business_data as dab
#         JOIN  cur_community.subdivisions as cs
#         ON ST_Contains(cs.shape, dab.geometry)
#         WHERE type = 'cabinet'
#     '''
#     return create_df(query)
#     # return dsu.run_query(query)

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