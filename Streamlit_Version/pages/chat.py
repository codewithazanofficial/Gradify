
import streamlit as st
import anthropic
import google.generativeai as genai
st.set_page_config(initial_sidebar_state="collapsed",page_title="AI Study Assistant", layout="centered")
st.markdown("""
<style>
[data-testid="stSidebarNav"] {
    display: none;
}
.stButton > button {
    background-color: #500073;
    color: white;
    font-size: 18px;
    font-weight: bold;
    padding: 0.6em 1.4em;
    border-radius: 10px;
    border: none;
    transition: 0.2s ease-in-out;
}
</style>
""", unsafe_allow_html=True)
genai.configure(api_key="AIzaSyBks6Zr8N8CQCIi42UsVBtR_VCmoumpEfo")
SYSTEM_PROMPT = """You are an Education and Lifestyle Assistant. Your role is to provide helpful, 
concise advice and information specifically about education and lifestyle topics.

Guidelines:
- Answer questions only about education (study tips, courses, learning strategies, academic topics, etc.) 
  and lifestyle (health, wellness, productivity, daily routines, habits, etc.)
- Keep answers brief and to the point (2-3 sentences when possible)
- If someone asks about topics outside education and lifestyle (movies, sports, politics, tech reviews, etc.), 
  politely decline and redirect them: "I'm specialized in education and lifestyle topics. I can't help with that, 
  but I'd be happy to discuss education or lifestyle-related questions!"
- Don't provide information about topics like entertainment, sports, news, or technical support unless 
  they relate to education or lifestyle
- Be friendly and helpful within your area of expertise"""
model = genai.GenerativeModel(model_name="gemini-2.5-flash", system_instruction=SYSTEM_PROMPT)

st.title("AI ASSISTANT")
st.caption("Ask anything about your studies")

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content":
         "You are a student marks predictor assistant. "
         "You analyze performance and give study advice."}
    ]

for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.chat_message("user").write(msg["content"])
    elif msg["role"] == "assistant":
        st.chat_message("assistant").write(msg["content"])

prompt = st.chat_input("Ask about your studies...")

if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    with st.chat_message("assistant"):
        placeholder = st.empty()
        full_text = ""

        history = []
        for m in st.session_state.messages:
            if m["role"] == "user":
                history.append({"role": "user", "parts": [m["content"]]})
            elif m["role"] == "assistant":
                history.append({"role": "model", "parts": [m["content"]]})
        try:
            response = model.generate_content(history, stream=True)
        except:
            st.error("Model not Available")
            response = None
        if response:
            for chunk in response:
                if chunk.text:
                    full_text += chunk.text
                    placeholder.markdown(full_text)

    st.session_state.messages.append({"role": "assistant", "content": full_text})
if st.sidebar.button("New Chat +"):
    st.session_state.messages = []
    st.rerun()
