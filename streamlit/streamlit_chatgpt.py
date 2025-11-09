import streamlit as st
import openai
from openai import OpenAI
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Set page config
st.set_page_config(
    page_title="ChatGPT Streamlit App",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize OpenAI client
@st.cache_resource
def get_openai_client():
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        st.error("Please set your OPENAI_API_KEY in a .env file.")
        st.stop()
    return OpenAI(api_key=api_key)

client = get_openai_client()

# Sidebar for settings
st.sidebar.title("Settings")
model = st.sidebar.selectbox(
    "Select Model",
    options=["gpt-3.5-turbo", "gpt-4o-mini", "gpt-4o"],
    index=0
)
temperature = st.sidebar.slider("Temperature", 0.0, 2.0, 0.7, 0.1)
max_tokens = st.sidebar.number_input("Max Tokens", min_value=50, max_value=2000, value=500)

# Clear chat button
if st.sidebar.button("Clear Chat History"):
    st.session_state.messages = []

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("What is your question?"):
    # Add user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate response
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""

        # Stream the response
        stream = client.chat.completions.create(
            model=model,
            messages=st.session_state.messages,
            temperature=temperature,
            max_tokens=max_tokens,
            stream=True,
        )

        for chunk in stream:
            if chunk.choices[0].delta.content is not None:
                full_response += chunk.choices[0].delta.content
                message_placeholder.markdown(full_response + "▌")

        message_placeholder.markdown(full_response)

    # Add assistant message to history
    st.session_state.messages.append({"role": "assistant", "content": full_response})

# Footer
st.sidebar.markdown("---")
st.sidebar.markdown("Built with Streamlit & OpenAI")