import streamlit as st

# Set the page title and header
st.title("Simple Calculator")

# Input fields for numbers
num1 = st.number_input("Enter the first number:", value=0.0)
num2 = st.number_input("Enter the second number:", value=0.0)

# Dropdown for selecting operation
operation = st.selectbox("Select operation:", ["+", "-", "*", "/"])

# Calculate button
if st.button("Calculate"):
    try:
        if operation == "+":
            result = num1 + num2
        elif operation == "-":
            result = num1 - num2
        elif operation == "*":
            result = num1 * num2
        elif operation == "/":
            if num2 == 0:
                st.error("Cannot divide by zero!")
                result = None
            else:
                result = num1 / num2
        
        if result is not None:
            st.success(f"Result: {result}")
    except Exception as e:
        st.error(f"An error occurred: {e}")