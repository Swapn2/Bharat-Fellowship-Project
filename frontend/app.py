import streamlit as st
import os
import sys

# Fix import path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from backend.chat_brain import chat_brain
from backend.data_fetcher import fetch_all_data
from backend.data_cleaner import clean_data

st.title("🤖 Project Samarth – Smart Agri Chatbot")

# ---- Section: Fetch & Clean ----
st.header("📥 Data Fetching & Cleaning")

state = st.text_input("Enter State Name")
district = st.text_input("Enter District Name")
commodity = st.text_input("Enter Commodity (optional)")

if st.button("Fetch & Clean Data"):
    try:
        df = fetch_all_data(state, district, commodity)
        if df.empty:
            st.warning("⚠️ No data fetched. Try different inputs.")
        else:
            cleaned_path = clean_data()
            st.success(f"✅ Data fetched and cleaned successfully! File: {cleaned_path}")
            st.session_state.cleaned_path = cleaned_path
    except Exception as e:
        st.error(f"❌ Error during fetch/clean: {e}")

# ---- Section: Available Analyses ----
st.header("📊 Available Analyses")

st.markdown("""
Here are some insights you can explore using the chatbot 👇  

1️⃣ **All distinct districts**  
2️⃣ **All distinct markets**  
3️⃣ **All distinct commodities**  
4️⃣ **Each commodity vs minimum, maximum & mean modal price**  
5️⃣ **Each commodity vs mean modal price**  
6️⃣ **Top 5 selling commodities**  

💡 *Example questions you can ask:*  
- "Show all distinct markets"  
- "Which commodity has the highest mean modal price?"  
- "Top 5 selling commodities in Uttar Pradesh"  
""")

# ---- Section: Chat Interface ----
st.header("💬 Chat with the Data")

user_input = st.text_input("Ask your question here (e.g., 'Show top 5 commodities')")

if st.button("Send"):
    if "cleaned_path" not in st.session_state:
        st.warning("⚠️ Please fetch and clean data first.")
    else:
        try:
            response = chat_brain(user_input, st.session_state.cleaned_path)
            st.write("### ✅ Response:")
            st.dataframe(response)
        except Exception as e:
            st.error(f"❌ Error while processing your query: {e}")
