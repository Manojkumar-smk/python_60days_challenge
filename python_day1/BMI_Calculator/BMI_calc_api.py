import streamlit as st
import requests

# Claude API configuration "include API key
API_KEY = "" 
API_URL = "https://api.anthropic.com/v1/messages"

def get_bmi_from_claude(weight, height):
    prompt = f"""You are a helpful assistant. Calculate the BMI for a person with:
- Weight: {weight} kg
- Height: {height} cm

Provide your response in this exact format:
1. BMI Category: [one word only - e.g., Underweight/Normal/Overweight/Obese]
2. Health Tips:
   - [One-line tip 1]
   - [One-line tip 2]

Keep it concise and actionable."""

    headers = {
        "x-api-key": API_KEY,
        "anthropic-version": "2023-06-01",
        "Content-Type": "application/json"
    }

    data = {
        "model": "claude-sonnet-4-5",
        "max_tokens": 300,
        "temperature": 0.5,
        "messages": [
            {"role": "user", "content": prompt}
        ]
    }

    response = requests.post(API_URL, headers=headers, json=data)
    if response.status_code == 200:
        return response.json()["content"][0]["text"]
    else:
        return f"Error: {response.status_code} - {response.text}"

# Streamlit UI
st.title("🤖 BMI Calculator with Claude AI")

weight = st.number_input("Enter your weight (kg)", min_value=1.0, step=0.1)
height = st.number_input("Enter your height (cm)", min_value=30.0, step=0.1)

if st.button("Calculate BMI"):
    with st.spinner("Asking Claude..."):
        result = get_bmi_from_claude(weight, height)
        st.success("Here's what Claude says:")
        st.write(result)
