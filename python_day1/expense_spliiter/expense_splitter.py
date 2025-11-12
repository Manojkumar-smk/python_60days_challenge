# expense_splitter_app.py
import streamlit as st
from decimal import Decimal, ROUND_HALF_UP
import pandas as pd
import io
import json
import base64
from typing import List, Dict

# --- Helper money functions (cents-based) ---
def to_cents(value: float) -> int:
    d = Decimal(str(value)).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
    return int((d * 100).to_integral_value(rounding=ROUND_HALF_UP))

def from_cents(cents: int) -> float:
    return float(Decimal(cents) / Decimal(100))

# --- Core logic ---
def compute_balances(total_amount: Decimal, number_of_people: int, participants: List[Dict]):
    total_cents = to_cents(float(total_amount))
    base_share = total_cents // number_of_people
    remainder = total_cents - base_share * number_of_people

    rows = []
    for i, p in enumerate(participants):
        contributed_cents = to_cents(float(p.get("contributed", 0.0)))
        extra = 1 if i < remainder else 0
        fair_share_cents = base_share + extra
        net_cents = contributed_cents - fair_share_cents
        rows.append({
            "name": p.get("name") or f"Person {i+1}",
            "contributed": from_cents(contributed_cents),
            "fair_share": from_cents(fair_share_cents),
            "net_balance": round(from_cents(net_cents), 2),  # positive => should receive
            "net_cents": net_cents
        })
    return rows

def generate_settlements(rows):
    # creditors: net_cents > 0, debtors: net_cents < 0
    creditors = [{"name": r["name"], "amount": r["net_cents"]} for r in rows if r["net_cents"] > 0]
    debtors = [{"name": r["name"], "amount": -r["net_cents"]} for r in rows if r["net_cents"] < 0]

    creditors.sort(key=lambda x: x["amount"], reverse=True)
    debtors.sort(key=lambda x: x["amount"], reverse=True)

    settlements = []
    ci = di = 0
    while di < len(debtors) and ci < len(creditors):
        debtor = debtors[di]
        creditor = creditors[ci]
        pay = min(debtor["amount"], creditor["amount"])
        if pay > 0:
            settlements.append({
                "from": debtor["name"],
                "to": creditor["name"],
                "amount": round(from_cents(pay), 2)
            })
        debtor["amount"] -= pay
        creditor["amount"] -= pay
        if debtor["amount"] == 0:
            di += 1
        if creditor["amount"] == 0:
            ci += 1
    return settlements

# --- Confetti helper (JS) ---
CONFETTI_HTML = """
<script src="https://cdn.jsdelivr.net/npm/canvas-confetti@1.5.1/dist/confetti.browser.min.js"></script>
<script>
  const duration = 3000;
  const animationEnd = Date.now() + duration;
  const defaults = { startVelocity: 30, spread: 360, ticks: 60, zIndex: 9999 };

  function fire() {
    const interval = setInterval(function() {
      const timeLeft = animationEnd - Date.now();
      if (timeLeft <= 0) {
        clearInterval(interval);
        return;
      }
      const particleCount = 50 * (timeLeft / duration);
      // since particles fall down, start a bit higher
      confetti(Object.assign({}, defaults, { particleCount, origin: { x: Math.random(), y: Math.random() - 0.2 } }));
    }, 250);
  }
  fire();
</script>
"""

# --- Streamlit UI ---
st.set_page_config(page_title="Expense Splitter", page_icon="💸", layout="wide")
st.title("💸 Expense Splitter — Interactive")
st.write("Enter total, participants and their contributions. The app computes fair shares and shows who pays whom. Click **Celebrate** for confetti!")

# Sidebar: quick controls & load/save
with st.sidebar:
    st.header("Group Controls")
    total_amount = st.number_input("Total amount", min_value=0.0, value=0.0, format="%.2f")
    num_people = st.number_input("Number of participants", min_value=1, value=2, step=1)
    st.markdown("---")
    st.markdown("Load / Save")
    uploaded = st.file_uploader("Upload participants JSON (optional)", type=["json", "txt"])
    if uploaded:
        try:
            uploaded_json = json.load(uploaded)
            # Save to session_state for main form to pick up
            st.session_state["_uploaded"] = uploaded_json
            st.success("Uploaded JSON loaded.")
        except Exception as e:
            st.error(f"Failed to parse JSON: {e}")

    if st.button("Reset saved inputs"):
        keys = [k for k in st.session_state.keys() if k.startswith("p_")]
        for k in keys:
            del st.session_state[k]
        st.success("Cleared participant inputs.")

# Build participants form with dynamic rows and memory
if "participants_count" not in st.session_state:
    st.session_state["participants_count"] = int(num_people)

# If the user changed num_people, update participants_count and initialize entries
if st.session_state["participants_count"] != int(num_people):
    prev = st.session_state["participants_count"]
    st.session_state["participants_count"] = int(num_people)
    # Initialize new keys as needed
    for i in range(int(num_people)):
        if f"p_name_{i}" not in st.session_state:
            st.session_state[f"p_name_{i}"] = f"Person {i+1}"
        if f"p_contrib_{i}" not in st.session_state:
            st.session_state[f"p_contrib_{i}"] = 0.0

# If uploaded JSON present, prefill
if "_uploaded" in st.session_state:
    up = st.session_state.pop("_uploaded")
    # expect structure with participants list, total_amount, number_of_people
    try:
        if "total_amount" in up:
            total_amount = up["total_amount"]
        if "number_of_people" in up:
            num_people = up["number_of_people"]
            st.session_state["participants_count"] = int(num_people)
        parts = up.get("participants", [])
        for i, p in enumerate(parts):
            st.session_state[f"p_name_{i}"] = p.get("name", f"Person {i+1}")
            st.session_state[f"p_contrib_{i}"] = float(p.get("contributed", 0.0))
    except Exception:
        st.warning("Uploaded JSON has unexpected structure — try a participants list.")

# Main participants area
st.subheader("👥 Participants")
participants = []
cols = st.columns([4,2,1])
with cols[0]:
    st.write("Name")
with cols[1]:
    st.write("Contribution")
with cols[2]:
    st.write("Remove?")

for i in range(int(num_people)):
    name_key = f"p_name_{i}"
    contrib_key = f"p_contrib_{i}"
    remove_key = f"p_remove_{i}"

    if name_key not in st.session_state:
        st.session_state[name_key] = f"Person {i+1}"
    if contrib_key not in st.session_state:
        st.session_state[contrib_key] = 0.0
    col1, col2, col3 = st.columns([4,2,1])
    with col1:
        st.session_state[name_key] = st.text_input(f"Name {i+1}", value=st.session_state[name_key], key=f"name_{i}")
    with col2:
        st.session_state[contrib_key] = st.number_input(f"Contribution {i+1}", min_value=0.0, value=float(st.session_state[contrib_key]), step=0.5, format="%.2f", key=f"contrib_{i}")
    with col3:
        if st.button("Remove", key=f"remove_{i}"):
            # mark removal by shifting later (simple approach: set contrib 0 and blank name)
            st.session_state[name_key] = ""
            st.session_state[contrib_key] = 0.0
            st.experimental_rerun()

    participants.append({
        "name": st.session_state[name_key] or f"Person {i+1}",
        "contributed": float(st.session_state[contrib_key])
    })

st.markdown("---")

# Options row
opt_col1, opt_col2, opt_col3 = st.columns(3)
with opt_col1:
    show_table = st.checkbox("Show participant table", value=True)
with opt_col2:
    enable_confetti = st.checkbox("Enable confetti on Celebrate", value=True)
with opt_col3:
    auto_celebrate_if_settled = st.checkbox("Auto-celebrate when fully settled (no one owes)", value=True)

# Calculation and results
if st.button("Calculate"):
    if total_amount <= 0:
        st.error("Please enter a total amount greater than 0.")
    elif int(num_people) <= 0:
        st.error("Number of participants must be at least 1.")
    else:
        rows = compute_balances(Decimal(str(total_amount)), int(num_people), participants)
        df = pd.DataFrame([{"Name": r["name"], "Contributed": r["contributed"], "Fair Share": r["fair_share"], "Net Balance": r["net_balance"]} for r in rows])

        # Summary metrics
        col_a, col_b, col_c, col_d = st.columns(4)
        total_contrib = sum([r["contributed"] for r in rows])
        with col_a:
            st.metric("Total Amount", f"₹{total_amount:.2f}")
        with col_b:
            st.metric("Total Contributed", f"₹{total_contrib:.2f}")
        with col_c:
            st.metric("People", f"{num_people}")
        with col_d:
            # show how many owe vs how many to receive
            owe_count = len([r for r in rows if r["net_cents"] < 0])
            recv_count = len([r for r in rows if r["net_cents"] > 0])
            st.metric("Owe / To Receive", f"{owe_count} / {recv_count}")

        st.markdown("**Details**")
        if show_table:
            # Use data_editor if available, otherwise fallback to dataframe
            try:
                # st.data_editor exists in newer streamlit versions
                st.data_editor(df, num_rows="fixed", use_container_width=True)
            except Exception:
                st.dataframe(df)

        settlements = generate_settlements(rows)
        st.markdown("**Settlements**")
        if settlements:
            for s in settlements:
                st.success(f"{s['from']} ➜ {s['to']}: ₹{s['amount']:.2f}")
        else:
            st.info("No settlements needed — everyone has paid their fair share!")

        # Download CSV
        csv = df.to_csv(index=False).encode("utf-8")
        st.download_button("Download participant table (CSV)", data=csv, file_name="expense_splitter_participants.csv", mime="text/csv")

        # Show "Celebrate" button & auto-confetti if settled
        celebrate = st.button("🎉 Celebrate")
        should_confetti = False
        if celebrate and enable_confetti:
            should_confetti = True
        if not settlements and auto_celebrate_if_settled and enable_confetti:
            # fully settled
            should_confetti = True

        if should_confetti:
            # Try streamlit balloons first (native)
            try:
                st.balloons()
            except Exception:
                # fallback to JS confetti embedded
                st.components.v1.html(CONFETTI_HTML, height=0)

        # Human-readable settlement suggestion block (copyable)
        st.markdown("---")
        st.subheader("Human-readable Summary")
        st.write("Fair share: each person should pay their fair share (shown below). Positive net = they should receive money; negative net = they owe money.")
        for r in rows:
            balance = r["net_balance"]
            if balance > 0:
                st.write(f"• **{r['name']}** should receive ₹{balance:.2f}")
            elif balance < 0:
                st.write(f"• **{r['name']}** owes ₹{abs(balance):.2f}")
            else:
                st.write(f"• **{r['name']}** is settled.")

        # Save the last result to session state for convenience
        st.session_state["_last_result"] = {
            "total_amount": float(total_amount),
            "number_of_people": int(num_people),
            "participants": [{"name": p["name"], "contributed": p["contributed"]} for p in participants],
            "rows": rows,
            "settlements": settlements
        }

# Quick restore / show last result
if st.session_state.get("_last_result"):
    if st.button("Show last result"):
        res = st.session_state["_last_result"]
        st.write(f"Last total: ₹{res['total_amount']:.2f}, People: {res['number_of_people']}")
        last_df = pd.DataFrame([{"Name": r["name"], "Contributed": r["contributed"], "Fair Share": r["fair_share"], "Net Balance": r["net_balance"]} for r in res["rows"]])
        st.dataframe(last_df)
        if res["settlements"]:
            st.write("Settlements:")
            for s in res["settlements"]:
                st.write(f"{s['from']} → {s['to']} : ₹{s['amount']:.2f}")
        else:
            st.info("No settlements were required.")

st.markdown("---")
st.caption("Expense Splitter — interactive Streamlit app. Built with care ❤️.")
