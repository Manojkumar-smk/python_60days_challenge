import streamlit as st

st.title("🎉 Greeting Form")

# Create a form
with st.form("greeting_form"):
    name = st.text_input("Enter your name", placeholder="John Doe")
    age = st.slider("Select your age", min_value=1, max_value=100, value=25)
    submitted = st.form_submit_button("Greet Me")

# Show greeting after submission
if submitted:
    if name.strip():
        st.success(f"Hello {name}! You are {age} years young 🎈")
    else:
        st.error("Please enter your name!")
