"""
- NEED TO MAP CHARACTERS TO ID's 
-  CREATE AND PERSIST PLAYERS WIN AND LOSS RECORD
- I WANT RANK SPECCFIC CHARACTER USAGE AND WIN LOSS RECORDS BY REGION 


"""

import streamlit as st
import pandas as pd
import plotly.express as px
import requests
import json
from datetime import datetime, timedelta

st.set_page_config(
  page_title="Tekken ananlysis",
  page_icon='👀',
  layout='wide'
 )

st.title("Tekken match analytics")