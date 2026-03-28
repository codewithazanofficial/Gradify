import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title='GRADIFY',initial_sidebar_state="collapsed")
st.markdown("""
<style>
[data-testid="stSidebarNav"] {
    display: none;
}
.stApp {
    background-color: #09122C;
    color: white;
}
.stButton > button {
    background-color: #6C63FF;
    color: white;
    font-size: 18px;
    font-weight: bold;
    padding: 0.6em 1.4em;
    border-radius: 10px;
    border: none;
    transition: 0.2s ease-in-out;
}

.stButton > button:hover {
    background-color: red;
    transform: scale(1.1);
}
input, textarea, select {
    background-color: #161b22 !important;
    color: white !important;
    border-radius: 8px !important;
    border: 1px solid #30363d !important;
    padding: 0.6em !important;
    font-size: 16px !important;
}

/* Focus effect */
input:focus, textarea:focus, select:focus {
    border-color: #6C63FF !important;
    box-shadow: 0 0 0 2px rgba(108,99,255,0.3) !important;
    outline: none !important;
}

/* Placeholder */
::placeholder {
    color: #8b949e !important;
}
</style>
""", unsafe_allow_html=True)
st.title("GRADIFY")

name = st.text_input("Name")

study_hours = st.number_input(
    "Study Hours Per Day",
    min_value=1,
    max_value=18
)

e_c_a_hours = st.number_input(
    "Extracurricular hours per day",
    min_value=0,
    max_value=8
)

sleep_hours = st.number_input(
    "Sleep hours per day",
    min_value=4,
    max_value=15
)

social_hours = st.number_input(
    "Social hours per day",
    min_value=0,
    max_value=15
)

physical_hours = st.number_input(
    "Physical hours per day",
    min_value=0,
    max_value=12
)

total = study_hours + e_c_a_hours + sleep_hours + social_hours + physical_hours

if total > 24:
    st.error(f"Total daily hours exceed 24 (currently {total}). Please adjust.")
    st.stop()
stress_level = st.selectbox('How much Stress Do You Feel', ['High', 'Medium', 'Low'])
stress_level = pd.Series({'stress_level' : stress_level})
stress_level = stress_level.map({'High': 0, 'Medium': 1, 'Low': 2})
stress_level = stress_level.values
user_text = st.text_input("How do you feel about studying this subject?")
if st.button("Submit", width='stretch'):
    user_data = {
    'user_data' : np.array([study_hours, e_c_a_hours, sleep_hours, social_hours,physical_hours, stress_level[0]]).reshape(1, -1),
    'user_text': user_text
    }
    st.session_state.user_data = user_data
    st.switch_page('pages/dashboard.py')

b1 = st.sidebar.button("AI ASSITANT", width='stretch')
if b1:
    st.switch_page("pages/chat.py")


