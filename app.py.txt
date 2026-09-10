import streamlit as st
import pandas as pd
from routing import get_coordinates, get_route_and_eta, fetch_route_hazards
from weather import get_current_weather
from ai_processor import generate_commute_briefing

st.set_page_config(page_title="Karachi Intelligent Route Navigator", page_icon="🚗", layout="centered")

st.title("🚗 Karachi Route Transit Navigator")
st.caption("Real-Time Route Geometry, Weather Profiling, & AI Commute Briefing (100% Free Stack)")

# 🛠️ Extract Secret API Keys securely from Streamlit Configuration context
try:
    GROQ_KEY = st.secrets["GROQ_API_KEY"]
    ORS_KEY = st.secrets["OPENROUTESERVICE_API_KEY"]
except Exception:
    st.error("Missing local API Secret Configuration credentials inside .streamlit/secrets.toml!")
    st.stop()

# --- STEP 1: USER INPUT INTERFACE ---
st.subheader("📍 Step 1: Define Your Commute")
col1, col2 = st.columns(2)
with col1:
    origin_input = st.text_input("Current Location / Starting Point", value="Clifton")
with col2:
    dest_input = st.text_input("Destination Point", value="Gulshan-e-Iqbal")

if st.button("Analyze Route Step-by-Step", type="primary"):
    
    # --- STEP 2: GEOCODING ---
    with st.status("Processing structural navigation telemetry...", expanded=True) as status:
        
        status.update(label="Locating coordinates on Karachi map layers...", state="running")
        start_coords = get_coordinates(origin_input)
        end_coords = get_coordinates(dest_input)
        
        if not start_coords or not end_coords:
            st.error("Failed to map coordinates for the chosen names. Please specify clear Karachi sector names.")
            st.stop()
            
        # --- STEP 3: ROUTING & PATH EXTRACTION ---
        status.update(label="Calculating optimal route polyline arrays...", state="running")
        route_telemetry = get_route_and_eta(start_coords, end_coords)
        
        if not route_telemetry:
            st.error("Could not construct an OSRM road bridge between points.")
            st.stop()
            
        # --- STEP 4: WEATHER INTEGRATION ---
        status.update(label="Extracting climatic conditions via Open-Meteo...", state="running")
        weather_profile = get_current_weather(end_coords)
        
        # --- STEP 5: HAZARD COMPILATION ---
        status.update(label="Scanning OpenRouteService for active route hurdles...", state="running")
        active_hazards = fetch_route_hazards(start_coords, ORS_KEY)
        
        status.update(label="All pipeline data points collected successfully!", state="complete")
        
    # --- DISPLAY METRICS & DETAILS ---
    st.success("### 📊 Your Core Commute Summary")
    
    m_col1, m_col2, m_col3 = st.columns(3)
    m_col1.metric("Est. Travel Time", f"{route_telemetry['duration_mins']} Mins")
    m_col2.metric("Destination Temp", f"{weather_profile['temp']} °C")
    m_col3.metric("Sky Condition", weather_profile['condition'])
    
    # --- STEP 6: AI GENERATED PREPARATION BRIEFING ---
    st.subheader("🧠 Mental Preparation Briefing (Powered by Groq)")
    with st.spinner("Generating humanized commute analysis..."):
        ai_briefing = generate_commute_briefing(
            GROQ_KEY, origin_input, dest_input, 
            route_telemetry['duration_mins'], weather_profile, active_hazards
        )
        st.info(ai_briefing)
        
    # --- STEP 7: STREAMLIT VISUAL MAP RENDERING ---
    st.subheader("🗺️ Path Trajectory View")
    map_df = pd.DataFrame(route_telemetry['path_points'], columns=['lat', 'lon'])
    st.map(map_df)
