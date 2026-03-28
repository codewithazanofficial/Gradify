import pickle
import streamlit as st
import os
 
st.set_page_config(initial_sidebar_state="collapsed", page_title="GRADIFY", layout="centered")
 
st.markdown("""
<style>
[data-testid="stSidebarNav"] { display: none; }
[data-testid="stSidebar"] { display: none; }
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
</style>
""", unsafe_allow_html=True)
 
from response import Response
 
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
 
with open(os.path.join(BASE_DIR, 'model_pickle'), 'rb') as f:
    lr_model = pickle.load(f)
 
st.title("GRADIFY || Dashboard")
 
if "user_data" in st.session_state and st.session_state.user_data:
    user_data = st.session_state.user_data
    r_esponse = Response(user_data)
    gpa = lr_model.predict(user_data['user_data'])
    adjusted_gpa = r_esponse.adjust_gpa(user_data['user_text'], gpa[0])
 
    if adjusted_gpa > 4:
        adjusted_gpa = 4
    elif adjusted_gpa < 1:
        adjusted_gpa = 1
    else:
        adjusted_gpa = round(float(adjusted_gpa), 2)
 
    st.success(adjusted_gpa)
 
    try:
        llm_response = r_esponse.generate_response(adjusted_gpa)
    except Exception as e:
        st.error(e)
        llm_response = None
 
    if llm_response:
        for sentence in llm_response:
            st.write(sentence)
 
else:
    st.warning("Nothing to Show. Please complete the survey first.")
    if st.button("← Go to Survey"):
        st.switch_page("frontend.py")
 
st.write("If you have any other queries or want advice from Gradify, click the button below:")
 
if st.button("🤖 ASK AI ASSISTANT"):
    st.switch_page("pages/chat.py")



# import pickle
# import streamlit as st
# import sys, os
# if "switch_page" not in st.session_state:
#     st.session_state.switch_page = False
# else:
#     st.switch_page("frontend.py")

# st.set_page_config(initial_sidebar_state="collapsed",page_title="GRADIFY", layout="centered")
# from response import Response
# BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# with open(os.path.join(BASE_DIR, 'model_pickle'), 'rb') as f:
#     lr_model = pickle.load(f)

# st.title("GRADIFY || Dashboard")
# if st.sidebar.button("AI ASSITANT"):
#     st.switch_page('frontend.py')
# if st.session_state.user_data:
#     user_data = st.session_state.user_data
#     r_esponse = Response(user_data)
#     gpa = lr_model.predict(user_data['user_data'])
#     adjusted_gpa = r_esponse.adjust_gpa(user_data['user_text'],gpa[0])
#     if adjusted_gpa > 4:
#         adjusted_gpa = 4
#     elif adjusted_gpa < 1:
#         adjusted_gpa = 1
#     else:
#         adjusted_gpa = f"{adjusted_gpa:.2f}"
#     st.success(adjusted_gpa)
#     try:
#         llm_response = r_esponse.generate_response(adjusted_gpa)
#     except Exception as e:
#         st.error(e)
#         llm_response = None
#     if llm_response:
#         for sentence in llm_response:
#             st.write(sentence)
#             Response.speak(sentence)
# else:
#     st.warning("Nothing to Show")

# st.write("I you have any other queries or you want to get an advice from Gradify click the button below:")
# if st.button("ASK AI ASSISTANT"):
#     st.session_state.switch_page = True