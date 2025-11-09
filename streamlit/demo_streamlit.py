import streamlit as st

st.title("My First Streamlit App")

name = st.text_input("Enter your name:")
if st.button("Greet me"):
    if name:
        st.success(f"Hello, {name}!, welcome to Streamlit.")
    else:
        st.warning("Please enter your name.")