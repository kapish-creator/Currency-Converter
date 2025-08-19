import streamlit as st
import requests

# ----------------- Helper Functions -----------------
def get_currencies():
    """Fetch all supported currencies."""
    url = "https://api.frankfurter.app/currencies"
    response = requests.get(url)
    return response.json()

def convert_currency(amount, from_currency, to_currency):
    """Convert amount from one currency to another."""
    if from_currency == to_currency:
        return amount
    url = f"https://api.frankfurter.app/latest?amount={amount}&from={from_currency}&to={to_currency}"
    response = requests.get(url)
    data = response.json()
    return data["rates"][to_currency]

# ----------------- Streamlit UI -----------------
st.set_page_config(page_title="🌍 Currency Converter", page_icon="💱", layout="centered")

# Custom CSS for responsiveness
st.markdown(
    """
    <style>
    .block-container {
        max-width: 700px;
        margin: auto;
        padding-top: 2rem;
    }
    h1 {
        font-size: 2rem !important;
        text-align: center;
        color: #2E86C1;
    }
    p, label {
        font-size: 1rem !important;
    }
    .stSuccess {
        font-size: 1.1rem !important;
    }
    @media (max-width: 600px) {
        h1 { font-size: 1.5rem !important; }
        .stSuccess { font-size: 1rem !important; }
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown("<h1>💱 Currency Converter</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center;color:gray;'>Real-time currency conversion powered by Frankfurter API</p>", unsafe_allow_html=True)

# Load available currencies
currencies = get_currencies()
currency_codes = list(currencies.keys())

# Always fixed base = MYR
base_currency = "MYR"

# Layout: Input currency + Target currency in columns
col1, col2 = st.columns(2)

with col1:
    input_currency = st.selectbox(
        "Currency you want to enter:",
        options=currency_codes,
        index=currency_codes.index("MYR") if "MYR" in currency_codes else 0,
        format_func=lambda x: f"{x} - {currencies[x]}"
    )

with col2:
    target_currency = st.selectbox(
        "Convert MYR to:",
        options=currency_codes,
        index=currency_codes.index("INR") if "INR" in currency_codes else 0,
        format_func=lambda x: f"{x} - {currencies[x]}"
    )

# Amount input
amount = st.number_input(f"Enter amount in {input_currency}:", min_value=0.0, step=0.1)

# Conversion
if amount:
    try:
        # Step 1: Convert input -> MYR
        amount_in_myr = convert_currency(amount, input_currency, base_currency)
        
        # Step 2: Convert MYR -> Target
        final_amount = convert_currency(amount_in_myr, base_currency, target_currency)

        st.success(
            f"💰 {amount:.2f} {input_currency} = {amount_in_myr:,.2f} {base_currency} "
            f"= {final_amount:,.2f} {target_currency}"
        )

    except Exception as e:
        st.error("⚠️ Unable to fetch live rates. Please try again later.")

# Footer
st.markdown(
    """
    <hr>
    <p style='text-align: center; color: gray;'>
    Data sourced from <a href='https://www.frankfurter.app/' target='_blank'>Frankfurter API</a> |
    Built with ❤️ using Streamlit
    </p>
    """,
    unsafe_allow_html=True
)
