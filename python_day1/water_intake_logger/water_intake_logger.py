import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Title
st.title("💧 Water Intake Tracker")
st.subheader("Track your daily hydration and progress toward 3L goal")

# Initialize session state
if "water_data" not in st.session_state:
    st.session_state.water_data = pd.DataFrame(columns=["Date", "Intake (ml)"])

# Layout: 3 columns
col1, col2, col3 = st.columns([1, 1, 2])

# Column 1: Input form
with col1:
    st.markdown("### 📝 Log Intake")
    with st.form("log_form"):
        date = st.date_input("Date")
        intake = st.number_input("Water Intake (ml)", min_value=0, step=100)
        submitted = st.form_submit_button("Log")
        if submitted:
            new_entry = pd.DataFrame([[date, intake]], columns=["Date", "Intake (ml)"])
            st.session_state.water_data = pd.concat(
                [st.session_state.water_data, new_entry], ignore_index=True
            )
            st.success(f"Logged {intake} ml for {date}")

# Column 2: Intake log
with col2:
    st.markdown("### 📋 Intake Log")
    if not st.session_state.water_data.empty:
        df = st.session_state.water_data.sort_values("Date")
        st.dataframe(df)
    else:
        st.info("No entries yet.")

# Column 3: Cumulative pie chart
with col3:
    st.markdown("### 🥧 Total Goal Completion")
    if not st.session_state.water_data.empty:
        df = st.session_state.water_data
        total_intake = df["Intake (ml)"].sum()
        unique_days = df["Date"].nunique()
        total_goal = 3000 * unique_days  # 3L per unique day

        achieved = min(total_intake, total_goal)
        remaining = max(total_goal - total_intake, 0)

        fig_pie, ax_pie = plt.subplots()
        ax_pie.pie(
            [achieved, remaining],
            labels=["Achieved", "Remaining"],
            colors=["#00BFFF", "#D3D3D3"],
            autopct="%1.1f%%",
            startangle=90,
        )
        ax_pie.set_title(f"Total Intake: {int(total_intake)} ml across {unique_days} day(s)")
        st.pyplot(fig_pie)
    else:
        st.info("Log water intake to see your chart.")
