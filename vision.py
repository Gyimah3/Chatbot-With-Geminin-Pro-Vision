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
def get_gemini_response(input, image):
    model = genai.GenerativeModel('gemini-pro-vision')
    response = model.generate_content([input, image])
    return response.text

# Function to handle sending messages
def send_message(message):
    if message and 'uploaded_image' in st.session_state and st.session_state.uploaded_image is not None:
        # Append user message to chat history
        st.session_state.chat_history.append(("You", message))
        # Get Gemini's response
        try:
            response = get_gemini_response(message, st.session_state.uploaded_image)
            st.session_state.chat_history.append(("Chatbot", response))
        except Exception as e:
            st.session_state.chat_history.append(("Chatbot", f"Error: {str(e)}"))
        # Rerun the app to update the chat display
        st.experimental_rerun()

# Initialize Streamlit app
st.set_page_config(page_title="Gideon's Image Chat")
st.sidebar.header("Instructions")
st.sidebar.write("Interact with the model like you would in a chat. Provide an image and ask questions!")

st.header("Gideon's Chat Application")

# Image uploader and persistence in session state
if 'uploaded_image' not in st.session_state:
    st.session_state.uploaded_image = None

uploaded_file = st.file_uploader("Upload an image...", type=["jpg", "jpeg", "png"])
if uploaded_file is not None:
    st.session_state.uploaded_image = Image.open(uploaded_file)
    st.image(st.session_state.uploaded_image, caption="Uploaded Image.", use_column_width=True)

# Initialize or get the chat history
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

# Chat UI
st.write("## Chat")
# Chat display area
chat_container = st.container()
for author, message in st.session_state.chat_history:
    color = 'blue' if author == "You" else 'green'
    chat_container.markdown(f"<span style='color: {color};'>{author}: {message}</span>", unsafe_allow_html=True)

# Chat input form
with st.form("chat_form", clear_on_submit=True):  # The form will clear the input on submit
    input_message = st.text_input("Your message:", key="input")
    submit_button = st.form_submit_button(label='Send')

# Handling form submission
if submit_button and input_message:
    send_message(input_message)

st.write("----")
st.header("Feedback")

# Feedback form
with st.form("feedback_form", clear_on_submit=True):  # Add clear_on_submit=True to clear the form on submit
    feedback = st.text_area("Your feedback", key="feedback_text")
    submitted_feedback = st.form_submit_button(label="Submit Feedback")

# Path to the feedback file
feedback_file_path = "feedback.txt"

if submitted_feedback and feedback:
    # Here you append the feedback to a text file in the current directory
    with open(feedback_file_path, "a") as file:
        file.write(f"Feedback: {feedback}\n")
    st.write("Thank you for your feedback!")

st.write("Privacy Notice: Your data is handled with confidentiality.")
