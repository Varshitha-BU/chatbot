
import os
import streamlit as st
from dotenv import load_dotenv
import google.generativeai as gen_ai

load_dotenv()

st.set_page_config(
    page_title="Gemini AI Chatbot",
    page_icon="🤖",
    layout="centered"
)

# Get API key from Streamlit Secrets or .env
GOOGLE_API_KEY = st.secrets.get(
    "GOOGLE_API_KEY",
    os.getenv("GOOGLE_API_KEY", "")
)

if not GOOGLE_API_KEY:
    st.error("Google API key is missing. Please configure your API key.")
    st.stop()

# Configure Gemini
gen_ai.configure(api_key=GOOGLE_API_KEY)

model = gen_ai.GenerativeModel("gemini-3.8-flash")

st.title("🤖 Gemini AI Chatbot")
st.caption("Chat with Google's Gemini AI")

# Initialize chat
if "chat_session" not in st.session_state:
    st.session_state.chat_session = model.start_chat(history=[])

# Display chat history
for message in st.session_state.chat_session.history:
    role = "assistant" if message.role == "model" else "user"
    with st.chat_message(role):
        st.markdown(message.parts[0].text)

# User input
user_prompt = st.chat_input("Ask anything...")

if user_prompt:
    with st.chat_message("user"):
        st.markdown(user_prompt)

    try:
        response = st.session_state.chat_session.send_message(user_prompt)

        with st.chat_message("assistant"):
            st.markdown(response.text)

    except Exception as e:
        st.error(f"Error: {e}")
