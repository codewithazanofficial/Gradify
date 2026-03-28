import pickle
import streamlit as st
import sys, os
if "switch_page" not in st.session_state:
    st.session_state.switch_page = False
else:
    st.switch_page("frontend.py")

st.set_page_config(initial_sidebar_state="collapsed",page_title="GRADIFY", layout="centered")
from response import Response
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

with open(os.path.join(BASE_DIR, 'model_pickle'), 'rb') as f:
    lr_model = pickle.load(f)

st.title("GRADIFY || Dashboard")
if st.sidebar.button("AI ASSITANT"):
    st.switch_page('frontend.py')
if st.session_state.user_data:
    user_data = st.session_state.user_data
    r_esponse = Response(user_data)
    gpa = lr_model.predict(user_data['user_data'])
    adjusted_gpa = r_esponse.adjust_gpa(user_data['user_text'],gpa[0])
    if adjusted_gpa > 4:
        adjusted_gpa = 4
    elif adjusted_gpa < 1:
        adjusted_gpa = 1
    else:
        adjusted_gpa = f"{adjusted_gpa:.2f}"
    st.success(adjusted_gpa)
    try:
        llm_response = r_esponse.generate_response(adjusted_gpa)
    except Exception as e:
        st.error(e)
        llm_response = None
    if llm_response:
        for sentence in llm_response:
            st.write(sentence)
            Response.speak(sentence)
else:
    st.warning("Nothing to Show")

st.write("I you have any other queries or you want to get an advice from Gradify click the button below:")
if st.button("ASK AI ASSISTANT"):
    st.session_state.switch_page = True