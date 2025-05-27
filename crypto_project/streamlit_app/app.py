import streamlit as st
import pandas as pd
import psycopg2
import matplotlib.pyplot as plt
import datetime

st.title("📊 Crypto Price Trends")

@st.cache_data
def load_data(coin):
    conn = psycopg2.connect(
        dbname="your_db_name",
        user="your_user",
        password="your_password",
        host="localhost",
        port="5433"
    )
    query = f"""
        SELECT timestamp, price_usd FROM crypto_prices
        WHERE coin_id = %s
        ORDER BY timestamp;
    """
    df = pd.read_sql(query, conn, params=(coin,))
    conn.close()
    return df

coin = st.selectbox("Choose a coin", ["bitcoin", "ethereum", "solana", "dogecoin"])
df = load_data(coin)

df['timestamp'] = pd.to_datetime(df['timestamp'])
df.set_index('timestamp', inplace=True)

# Moving average
df['ma'] = df['price_usd'].rolling(window=5).mean()

st.line_chart(df[['price_usd', 'ma']])

st.subheader("📌 Buy/Sell Suggestions")
minima = df[df['price_usd'] == df['price_usd'].rolling(3, center=True).min()]
maxima = df[df['price_usd'] == df['price_usd'].rolling(3, center=True).max()]

st.write("💡 Local Minima (Potential Buy):")
st.write(minima.tail())

st.write("💡 Local Maxima (Potential Sell):")
st.write(maxima.tail())
