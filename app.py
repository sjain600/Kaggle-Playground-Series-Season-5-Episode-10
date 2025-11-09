import streamlit as st
import pandas as pd
import numpy as np
import joblib
import random

# Page configuration
st.set_page_config(page_title='Accident Risk Prediction', page_icon='🚘', layout='wide')
st.title('🚘Interactive Accident Risk Predictor')
st.write('Adjust the sliders and dropdown below')

# Layout: Input (Left) and Output (Right)
left_col, right_col = st.columns([1.3, 1])

with left_col:
    st.subheader('Input Road & Environment Details')
    
    col1, col2 = st.columns(2)
    with col1:
        num_lanes = st.slider('Number of Lanes', 1, 4)
        curvature = st.slider('Curvature', 0.0, 1.0)
        speed_limit = st.slider('Speed Limit', 35, 100)
        lighting = st.selectbox('Lighting Condition', ['daylight', 'dim', 'night'])
        weather = st.selectbox('Weather Condition', ['clear', 'rain', 'foggy'])
        road_signs_present = st.selectbox('Road Signs Present', [True, False])
        
        
    with col2:
        public_road = st.selectbox('Is it a Public Road?', [True, False])
        time_of_day = st.selectbox('Time of Day', ['morning', 'afternoon', 'evening'])
        holiday = st.selectbox('Is it a Holiday?', [True, False])
        school_season = st.selectbox('Is it School Season Active?', [True, False])
        num_reported_accidents = st.number_input('Number of Reported Accidents', 0, 7)
        road_type = st.selectbox('Road Type', ['rural', 'urban', 'highway'])
        
def generate_synthetic_data(num_rows=10000, seed=42):
    np.random.seed(seed)
    random.seed(seed)

    data = {
        "road_type" : np.random.choice(["highway", "urban","rural"], num_rows),
        "num_lanes" : np.random.randint(1, 5, num_rows),
        "curvature" : np.round(np.random.uniform(0.0, 1.0, num_rows), 2),
        "speed_limit" : np.random.choice([25, 35, 45, 60, 70],num_rows),
        "lighting" : np.random.choice(["daylight", "night", "dim"], num_rows),
        "weather" : np.random.choice(["clear", "rainy", "foggy"], num_rows),
        "road_signs_present" : np.random.choice([True, False], num_rows),
        "public_road" : np.random.choice([True, False], num_rows),
        "time_of_day" : np.random.choice(["morning", "evening", "afternoon"], num_rows),
        "holiday" : np.random.choice([True, False], num_rows),
        "school_season" : np.random.choice([True, False], num_rows),
        "num_reported_accidents" : np.random.poisson(lam=1.5, size=num_rows)
    }

    # simulate risk score  influenced by  features + noise
    base_risk = (
        0.3 * data["curvature"] + 
        0.2 * (data["lighting"] == "night").astype(int) + 
        0.1 * (data["weather"] != "clear").astype(int) + 
        0.2 * (data["speed_limit"] >= 60).astype(int) + 
        0.1 * (np.array(data["num_reported_accidents"]) > 2).astype(int)
    )
    
    noise = np.random.normal(0, 0.05, num_rows)
    risk_score = np.clip(base_risk + noise, 0, 1)
    data["accident_risk"] = np.round(risk_score, 2)

    return pd.DataFrame(data)

df = generate_synthetic_data(num_rows=10000)
        
        

        
