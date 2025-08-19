import streamlit as st
import requests

# ----------------- Helper Functions -----------------
def get_currencies():
    """Fetch all supported currencies."""
    url = "https://api.frankfurter.app/currencies"
    response = requests.get(url)
    return response.json()

def convert_currency(amount, from_currency, to_currency):
    """Convert amount from one currency to another directly."""
    if from_currency == to_currency:
        return amount
    url = f"https://api.frankfurter.app/latest?amount={amount}&from={from_currency}&to={to_currency}"
    response = requests.get(url)
    data = response.json()
    return data["rates"][to_currency]

# ----------------- Streamlit UI -----------------
st.set_page_config(page_title="Currency Converter", page_icon="💱", layout="centered")

st.title("💱 Global Currency Converter")
st.caption("Real-time currency conversion powered by Frankfurter API")

# Load currencies
currencies = get_currencies()
currency_codes = list(currencies.keys())

# Columns for input and target currency
col1, col2 = st.columns(2)

with col1:
    input_currency = st.selectbox(
        "Currency you want to enter:",
        options=currency_codes,
        index=currency_codes.index("MYR") if "MYR" in currency_codes else 0,  # Default MYR
        format_func=lambda x: f"{x} - {currencies[x]}"
    )

with col2:
    target_currency = st.selectbox(
        f"Convert {input_currency} to:",
        options=currency_codes,
        index=currency_codes.index("INR") if "INR" in currency_codes else 0,
        format_func=lambda x: f"{x} - {currencies[x]}"
    )

# Amount input
amount = st.number_input(f"Enter amount in {input_currency}:", min_value=0.0, step=0.1)

# Conversion
if amount:
    try:
        final_amount = convert_currency(amount, input_currency, target_currency)
        st.success(
            f"💰 {amount:.2f} {input_currency} = {final_amount:,.2f} {target_currency}"
        )
    except Exception:
        st.error("⚠️ Unable to fetch live rates. Please try again later.")

# Footer
st.markdown("---")
st.markdown(
    "Data sourced from [Frankfurter API](https://www.frankfurter.app/) | Built with ❤️ using Streamlit",
    unsafe_allow_html=True,
)
