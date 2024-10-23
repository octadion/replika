import streamlit as st
import threading
from agents import AICompanionAgent, EntitiesExtractionAgent
from prompts import COMPANION_PROMPT_TEMPLATE
from tools import entities_extraction_tools

companion_agent = AICompanionAgent(COMPANION_PROMPT_TEMPLATE, verbose=False)
user_profile_updater = EntitiesExtractionAgent(tools=entities_extraction_tools)

st.title("emotionalAI")

if 'history' not in st.session_state:
    st.session_state.history = []

def handle_input(user_input):
    profile_update_thread = threading.Thread(
        target=user_profile_updater.update_user_profile, args=(user_input,))
    profile_update_thread.start()

    ai_response = companion_agent.talk(user_input)

    st.session_state.history.append(("Human", user_input))
    st.session_state.history.append(("AI", ai_response))

user_input = st.chat_input("You:")
if user_input:
    handle_input(user_input)

if st.session_state.history:
    for speaker, message in st.session_state.history:
        if speaker == "Human":
            st.chat_message("user").markdown(f"**You:** {message}")
        else:
            st.chat_message("AI").markdown(f"**AI:** {message}")
