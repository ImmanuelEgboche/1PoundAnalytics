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

CHARACTER_MAP = {
    1: "Jin", 2: "Kazuya", 3: "Nina", 4: "Paul", 5: "Law", 6: "King", 7: "Yoshimitsu",
    8: "Hwoarang", 9: "Xiaoyu", 10: "Heihachi", 11: "Claudio", 12: "Shaheen", 
    13: "Josie", 14: "Devil Jin", 15: "Jack-8", 16: "Asuka", 17: "Leroy", 
    18: "Lili", 19: "Bryan", 20: "Alisa", 21: "Feng", 22: "Panda", 23: "Lee",
    24: "Lars", 25: "Zafina", 26: "Ganryu", 27: "Julia", 28: "Master Raven",
    29: "Noctis", 30: "Geese", 31: "Negan", 32: "Fahkumram", 33: "Kunimitsu",
    34: "Lidia", 35: "Akuma", 36: "Eliza", 37: "Miguel", 38: "Leo", 39: "Steve",
    40: "Dragunov", 41: "Kuma", 42: "Reina", 43: "Azucena"
}

REGION_MAP = {
    0: "Japan", 1: "Korea", 2: "Asia", 3: "North America", 
    4: "Europe", 5: "South America", 6: "Other"
}

st.set_page_config(
  page_title="Tekken ananlysis",
  page_icon='👀',
  layout='wide'
 )

st.title("Tekken match analytics")

st.sidebar.header("Controls")
refresh_data = st.sidebar.button('Refresh Data')


@st.cache_data(ttl=3600)
def load_match_data():
    try:
        with open('results.json', 'r') as f:
            raw_data = json.load(f)

        result = {
            'matches': raw_data, 
            'last_updated': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }

    

        
        processed_matches = []

        for match in raw_data:
            battle_date = datetime.fromtimestamp(match['battle_at'])

            p1_character = CHARACTER_MAP.get(match['p1_chara_id'], f"Unknown_{match['p1_chara_id']}")

            p2_character = CHARACTER_MAP.get(match['p2_chara_id'], f"Unknown_{match['p2_chara_id']}")

            p1_region = REGION_MAP.get(match.get('p1_region_id'), "Unknown") if match.get('p1_region_id') is not None else "Unknown"

            p2_region = REGION_MAP.get(match.get('p2_region_id'), "Unknown") if match.get('p2_region_id') is not None else "Unknown"


            processed_match = {
                    'battle_id': match['battle_id'],
                    'date': battle_date,
                    'p1_name': match['p1_name'],
                    'p1_chara_id': p1_character,
                    'p1_power': match['p1_power'],
                    'p1_rank': match['p1_rank'],
                    'p1_rounds': match['p1_rounds'],
                    'p1_region': p1_region,
                    'p2_name': match['p2_name'], 
                    'p2_chara_id': p2_character,
                    'p2_power': match['p2_power'],
                    'p2_rank': match['p2_rank'],
                    'p2_rounds': match['p2_rounds'],
                    'p2_region': p2_region,
                    'winner': match['winner'],
                    'total_rounds': match['p1_rounds'] + match['p2_rounds'],
                    'battle_type': match['battle_type']
                }

            processed_matches.append(processed_match)

        
        return {

                'matches': processed_matches,
                'last_updated': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'total_matches': len(processed_matches)
            }

    except FileNotFoundError:
        st.error("JSON file not found. Please upload your json file.")
        st.stop()
        return None
    except Exception as e:
        st.error(f'Error loading data: {e}')
        st.stop()
    
data = load_match_data()

df = pd.DataFrame(data['matches'])

if not df.empty:
    st.write("First row keys:", df.iloc[0].to_dict().keys())
    st.write("Has total_rounds?", 'total_rounds' in df.columns)

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Total Matches", len(df))

with col2:
    st.write(df) 
    unique_characters = len(pd.concat([df['p1_chara_id'], df['p2_chara_id']]).unique())
    st.metric("Unique Charcters", unique_characters)

with col3:
    avg_rounds = df['total_rounds'].mean()
    st.metric('Avg Rounds/Match', f"{avg_rounds:.1f}")

with col4:
    st.metric("Last Updated", data['last_updated'])

st.markdown("---")

