from dotenv import load_dotenv
import os
import streamlit as st
from PIL import Image
import google.generativeai as genai

# Load API key from environment variables
google_api_key = st.secrets["GOOGLE_API_KEY"]
genai.configure(api_key=google_api_key)

# GOOGLE_API_KEY = st.secrets["GOOGLE_API_KEY"]
# genai.configure(api_key=GOOGLE_API_KEY)


# Function to load OpenAI model and get responses
def get_gemini_response(input_text):
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content([input_text])
    return response.text

# Function to handle sending messages with greeting response and context memory
def send_message(message):
    if message:
        # Append user message to chat history
        st.session_state.chat_history.append(("You", message))

        # Check for greetings and respond without calling the external API
        if message.strip().lower() in ["hi", "hello", "hey"]:
            greeting_response = "Hello! How can I help you today?"
            st.session_state.chat_history.append(("Chatbot", greeting_response))
            st.session_state['last_bot_response'] = greeting_response  # Store last bot response
        else:
            # Prepare context for the message if available
            context = st.session_state.get('last_bot_response', '')
            full_message = f"{context} {message}" if context else message

            # Get Gemini's response for non-greeting messages
            try:
                response = get_gemini_response(full_message)
                st.session_state.chat_history.append(("Chatbot", response))
                st.session_state['last_bot_response'] = response  # Update last bot response
            except Exception as e:
                st.session_state.chat_history.append(("Chatbot", f"Error: {str(e)}"))

        # Rerun the app to update the chat display
        st.experimental_rerun()

# Initialize Streamlit app and session state for chat history
st.set_page_config(page_title="Gideon's Chat Application")
st.sidebar.header("Instructions")
st.sidebar.write("Interact with the model by typing in your message! Please note that this Chatbot cannot keep memory of immediate chat.")

st.header("Gideon's Chat Application")

if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

# Display chat history
st.write("## Chat")
chat_container = st.container()
with chat_container:
    for author, message in st.session_state.chat_history:
        if author == "You":
            chat_container.markdown(f"<span style='color: blue;'>{author}:</span> {message}", unsafe_allow_html=True)
        else:  # "Chatbot"
            chat_container.markdown(f"<span style='color: green;'>{author}:</span> {message}", unsafe_allow_html=True)

# Use st.chat_input for direct messaging
user_message = st.chat_input("Say something", key="chat_input")
if user_message:
    send_message(user_message)
