# app.py

import streamlit as st
import requests
from datetime import datetime
from zoneinfo import ZoneInfo
import json

st.set_page_config(
    page_title="AstroAI ✨",
    page_icon="✨",
    layout="centered",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@500;700&family=Poppins:wght@300;400;500&display=swap');
    
    .main {background: linear-gradient(135deg, #1a0b3d 0%, #2d1b69 50%, #000428 100%); color: #e6e6fa;}
    h1 {font-family: 'Playfair Display', serif; color: #ffd700; text-align: center; font-size: 3.5rem; margin-bottom: 0.5rem;}
    h3 {font-family: 'Playfair Display', serif; color: #b19cd9;}
    .stTextInput > div > div > input {background: rgba(255,255,255,0.1); border: 1px solid #9370db; color: white; border-radius: 12px;}
    .stDateInput > div > div > input, .stTimeInput > div > div > input {background: rgba(255,255,255,0.1); color: white; border-radius: 12px;}
    .stSelectbox > div > div {background: rgba(255,255,255,0.1); border-radius: 12px;}
    .result-box {
        background: linear-gradient(145deg, rgba(138,43,226,0.3), rgba(75,0,130,0.4));
        padding: 2rem;
        border-radius: 20px;
        border: 1px solid rgba(255,215,0,0.3);
        box-shadow: 0 10px 30px rgba(138,43,226,0.4);
        margin: 2rem 0;
        text-align: center;
    }
    .zodiac-header {font-size: 2.8rem; color: #ffd700; text-shadow: 0 0 20px #ffd700;}
    .insight-text {font-family: 'Poppins', sans-serif; font-size: 1.4rem; line-height: 1.8; color: #e6e6fa;}
    .caption {color: #b19cd9; font-style: italic;}
    .stButton>button {
        background: linear-gradient(45deg, #9c27b0, #e91e63);
        color: white;
        font-weight: bold;
        border: none;
        border-radius: 50px;
        padding: 0.8rem 2.5rem;
        font-size: 1.2rem;
        box-shadow: 0 8px 20px rgba(156,39,176,0.5);
        transition: all 0.3s;
    }
    .stButton>button:hover {
        transform: translateY(-3px);
        box-shadow: 0 12px 30px rgba(156,39,176,0.7);
    }
</style>
""", unsafe_allow_html=True)

@st.cache_resource
def load_cities():
    try:
        with open("city+state+india.json", "r", encoding="utf-8") as f:
            data = json.load(f)
        locations = [f"{item['city']}, {item['state']}, India" for item in data]
        return sorted(set(locations))
    except:
        return ["Delhi, Delhi, India"]

ALL_LOCATIONS = load_cities()

st.markdown("<h1>✨ AstroAI ✨</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #b19cd9; font-size:1.2rem;'>Your AI-powered cosmic guidance in 11 Indian languages</p>", unsafe_allow_html=True)
st.markdown("---")

with st.container():
    col1, col2 = st.columns(2)
    with col1:
        name = st.text_input("Your Name", placeholder="e.g. Vishal Gaur", help="How would you like to be addressed?")
        birth_date = st.date_input("Birth Date", datetime(2000, 6, 10), min_value=datetime(1900,1,1))
    with col2:
        birth_time = st.time_input(
            "Birth Time",
            value=datetime.strptime("00:30", "%H:%M").time(),
            step=60
        )
        birth_place = st.selectbox("Birth Place", options=ALL_LOCATIONS, index=ALL_LOCATIONS.index("Hathras, Uttar Pradesh, India") if "Hathras, Uttar Pradesh, India" in ALL_LOCATIONS else 0)

    lang = st.selectbox("Language", [
        "en", "hi", "ta", "te", "bn", "gu", "kn", "ml", "pa", "mr", "ur"
    ], format_func=lambda x: {
        "en": "English", "hi": "हिंदी", "ta": "தமிழ்", "te": "తెలుగు",
        "bn": "বাংলা", "gu": "ગુજરાતી", "kn": "ಕನ್ನಡ", "ml": "മലയാളം",
        "pa": "ਪੰਜਾਬੀ", "mr": "मराठी", "ur": "اردو"
    }[x])

    submit = st.button("START", use_container_width=True, type="primary")

if submit:
    if not name.strip():
        st.error("✗ Please enter your name")
    else:
        with st.spinner("Consulting the stars and planets..."):
            payload = {
                "name": name.strip(),
                "birth_date": birth_date.strftime("%Y-%m-%d"),
                "birth_time": birth_time.strftime("%H:%M"),
                "birth_place": birth_place,
                "language": lang
            }
            try:
                response = requests.post("http://127.0.0.1:8000/predict", json=payload, timeout=90)
                data = response.json()

                if response.status_code != 200 or "error" in data:
                    st.error(data.get("error", "Something went wrong. Try again."))
                else:
                    st.balloons()
                    st.success("✨ Your cosmic message has arrived from the universe!")

                    st.markdown(f"""
                    <div class="result-box">
                        <div class="zodiac-header">♈ {data['zodiac']} ♌</div>
                        <p class="insight-text" style="
                            font-size:1.3rem;
                            line-height:1.9;
                            color:#f3eaff;
                            text-shadow:0 0 12px rgba(255,215,255,0.4);
                            letter-spacing:0.3px;
                        ">
                            “{data['insight']}”
                        </p>
                        <p class="caption" style="font-size:1.1rem; text-align:center;">
                            <span style="color:#ffd700;">⏱ {datetime.now(ZoneInfo("Asia/Kolkata")).strftime("%H:%M")} IST</span>
                        </p>
                    </div>
                    """, unsafe_allow_html=True)

            except requests.ConnectionError:
                st.error("Backend server is not running! Run: `python api.py`")
            except requests.Timeout:
                st.error("The stars are taking time... Please try again.")
            except Exception as e:
                st.error(f"Unexpected error: {e}")