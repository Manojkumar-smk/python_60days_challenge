import streamlit as st

# Unit Conversion Functions
def length_conversion(value, from_unit, to_unit):
    # Convert to meters first
    to_meters = {
        "Millimeter": 0.001,
        "Centimeter": 0.01,
        "Meter": 1,
        "Kilometer": 1000,
        "Inch": 0.0254,
        "Foot": 0.3048,
        "Yard": 0.9144,
        "Mile": 1609.34
    }
    
    meters = value * to_meters[from_unit]
    result = meters / to_meters[to_unit]
    return result

def weight_conversion(value, from_unit, to_unit):
    # Convert to kilograms first
    to_kg = {
        "Milligram": 0.000001,
        "Gram": 0.001,
        "Kilogram": 1,
        "Metric Ton": 1000,
        "Ounce": 0.0283495,
        "Pound": 0.453592,
        "Stone": 6.35029
    }
    
    kg = value * to_kg[from_unit]
    result = kg / to_kg[to_unit]
    return result

def temperature_conversion(value, from_unit, to_unit):
    # Convert to Celsius first
    if from_unit == "Celsius":
        celsius = value
    elif from_unit == "Fahrenheit":
        celsius = (value - 32) * 5/9
    elif from_unit == "Kelvin":
        celsius = value - 273.15
    
    # Convert from Celsius to target unit
    if to_unit == "Celsius":
        result = celsius
    elif to_unit == "Fahrenheit":
        result = (celsius * 9/5) + 32
    elif to_unit == "Kelvin":
        result = celsius + 273.15
    
    return result

def volume_conversion(value, from_unit, to_unit):
    # Convert to liters first
    to_liters = {
        "Milliliter": 0.001,
        "Liter": 1,
        "Cubic Meter": 1000,
        "Gallon (US)": 3.78541,
        "Gallon (UK)": 4.54609,
        "Fluid Ounce (US)": 0.0295735,
        "Cup": 0.236588,
        "Pint": 0.473176,
        "Quart": 0.946353
    }
    
    liters = value * to_liters[from_unit]
    result = liters / to_liters[to_unit]
    return result

# Streamlit UI
st.title("🔄 Unit Converter")
st.write("Convert between different units easily!")

# Sidebar for category selection
st.sidebar.header("Select Conversion Type")
conversion_type = st.sidebar.selectbox(
    "Choose Category",
    ["Length", "Weight", "Temperature", "Volume"]
)

# Main content
col1, col2 = st.columns(2)

if conversion_type == "Length":
    units = ["Millimeter", "Centimeter", "Meter", "Kilometer", "Inch", "Foot", "Yard", "Mile"]
    
    with col1:
        st.subheader("From")
        value = st.number_input("Enter value", min_value=0.0, value=1.0, step=0.01, key="length_value")
        from_unit = st.selectbox("From Unit", units, key="length_from")
    
    with col2:
        st.subheader("To")
        to_unit = st.selectbox("To Unit", units, index=2, key="length_to")
        result = length_conversion(value, from_unit, to_unit)
        st.metric("Result", f"{result:.6f} {to_unit}")

elif conversion_type == "Weight":
    units = ["Milligram", "Gram", "Kilogram", "Metric Ton", "Ounce", "Pound", "Stone"]
    
    with col1:
        st.subheader("From")
        value = st.number_input("Enter value", min_value=0.0, value=1.0, step=0.01, key="weight_value")
        from_unit = st.selectbox("From Unit", units, key="weight_from")
    
    with col2:
        st.subheader("To")
        to_unit = st.selectbox("To Unit", units, index=2, key="weight_to")
        result = weight_conversion(value, from_unit, to_unit)
        st.metric("Result", f"{result:.6f} {to_unit}")

elif conversion_type == "Temperature":
    units = ["Celsius", "Fahrenheit", "Kelvin"]
    
    with col1:
        st.subheader("From")
        value = st.number_input("Enter value", value=0.0, step=0.1, key="temp_value")
        from_unit = st.selectbox("From Unit", units, key="temp_from")
    
    with col2:
        st.subheader("To")
        to_unit = st.selectbox("To Unit", units, index=1, key="temp_to")
        result = temperature_conversion(value, from_unit, to_unit)
        st.metric("Result", f"{result:.2f} {to_unit}")

elif conversion_type == "Volume":
    units = ["Milliliter", "Liter", "Cubic Meter", "Gallon (US)", "Gallon (UK)", "Fluid Ounce (US)", "Cup", "Pint", "Quart"]
    
    with col1:
        st.subheader("From")
        value = st.number_input("Enter value", min_value=0.0, value=1.0, step=0.01, key="volume_value")
        from_unit = st.selectbox("From Unit", units, key="volume_from")
    
    with col2:
        st.subheader("To")
        to_unit = st.selectbox("To Unit", units, index=1, key="volume_to")
        result = volume_conversion(value, from_unit, to_unit)
        st.metric("Result", f"{result:.6f} {to_unit}")

# Add some styling
st.markdown("---")
st.markdown("### Quick Reference")
st.info("""
**Supported Conversions:**
- 📏 Length: mm, cm, m, km, in, ft, yd, mi
- ⚖️ Weight: mg, g, kg, ton, oz, lb, stone
- 🌡️ Temperature: °C, °F, K
- 🧪 Volume: ml, L, m³, gal, fl oz, cup, pint, quart
""")
