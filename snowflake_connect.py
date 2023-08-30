import os
import snowflake.connector
import streamlit as st
from dotenv import load_dotenv 

load_dotenv() # TODO: move to dsu package

# PASSWORD = os.getenv('SNOWSQL_PWD')
# WAREHOUSE = os.getenv('WAREHOUSE')
# USER = os.getenv('USER')

PASSWORD = "Jigsaw23"
WAREHOUSE = "COMPUTE_WH"
USER = "SONYAK"

# ctx = snowflake.connector.connect(
#     user='SonyaK',
#     password=PASSWORD
#     # account='myorganization-myaccount',
#     )

conn = snowflake.connector.connect(
    user=USER,
    password=PASSWORD,
    # account=ACCOUNT,
    warehouse=WAREHOUSE,
    database="B2BCONNECT__BUSINESS_FIRMOGRAPHICS_DEMOSAMPLE"
    # schema=SCHEMA
    )

conn.cursor().execute("select * from dataset.mdsusbusinesssample_view limit 1")