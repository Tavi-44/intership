import streamlit as st
import gdown
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
st.set_page_config(page_title="Trader Performance Dashboard", layout="wide")
st.title("📊 Trader Performance vs Market Sentiment")
@st.cache_data
def load_data():
    file_id = "1T3oKb46tkYlXOTEUrY3UvoAcPIYZy6g7"
    url = f"https://drive.google.com/uc?id={file_id}"
    output = "merged_data.csv"
    gdown.download(url, output, quiet=False)
    df = pd.read_csv(output)
    return df
df = load_data()
df = df.dropna(subset=['sentiment'])
st.sidebar.header("Filters")
sentiment_filter = st.sidebar.multiselect(
    "Select Sentiment",
    options=df['sentiment'].unique(),
    default=df['sentiment'].unique()
)
filtered_df = df[df['sentiment'].isin(sentiment_filter)]
st.subheader("📌 Key Metrics")
col1, col2, col3 = st.columns(3)
col1.metric("Avg PnL", round(filtered_df['Closed PnL'].mean(), 2))
col2.metric("Win Rate", round((filtered_df['Closed PnL'] > 0).mean(), 2))
col3.metric("Total Trades", filtered_df.shape[0])
st.subheader("📈 Avg PnL: Fear vs Greed")
pnl_data = filtered_df.groupby('sentiment')['Closed PnL'].mean()
fig, ax = plt.subplots()
pnl_data.plot(kind='bar', ax=ax)
st.pyplot(fig)
st.subheader("🏆 Win Rate")
win_data = filtered_df.groupby('sentiment')['Closed PnL'].apply(lambda x: (x > 0).mean())
fig, ax = plt.subplots()
win_data.plot(kind='bar', ax=ax)
st.pyplot(fig)
st.subheader("📊 Trade Frequency Over Time")
freq_data = filtered_df.groupby(['date','sentiment']).size().unstack()
fig, ax = plt.subplots()
freq_data.plot(ax=ax)
st.pyplot(fig)
st.subheader("⚖️ Long vs Short")
side_data = filtered_df.groupby(['sentiment','Side']).size().unstack()
fig, ax = plt.subplots()
side_data.plot(kind='bar', ax=ax)
st.pyplot(fig)
st.subheader("💰 Trade Size Impact")
median_size = filtered_df['Size USD'].median()
filtered_df['size_type'] = np.where(filtered_df['Size USD'] > median_size, 'High', 'Low')
size_data = filtered_df.groupby(['size_type','sentiment'])['Closed PnL'].mean().unstack()
fig, ax = plt.subplots()
size_data.plot(kind='bar', ax=ax)
st.pyplot(fig)
st.markdown("---")
st.markdown("Made by Tanmay 🚀")
