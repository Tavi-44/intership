import streamlit as st
import gdown
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
st.set_page_config(page_title="Trader Performance Dashboard", layout="wide")
st.title("📊 Trader Performance vs Market Sentiment")
@st.cache_data
# Set page config (emoji hata diya temporary)
st.set_page_config(page_title="Trader Performance Dashboard", layout="wide")

st.title("Trader Performance vs Market Sentiment")

# 1️⃣ File uploader (outside any cached function)
uploaded_file = st.file_uploader("Upload your merged CSV", type=["csv"])

# 2️⃣ Load data using cache (optional)
@st.cache_data
def load_data(file):
    df = pd.read_csv(file)
    return df

# 3️⃣ Check if file is uploaded
if uploaded_file is not None:
    df = load_data(uploaded_file)
    df = df.dropna(subset=['sentiment'])  # remove rows with missing sentiment
    st.write(df.head())
    
    # Example plot
    st.subheader("Sentiment distribution")
    st.bar_chart(df['sentiment'].value_counts())
else:
    st.warning("Please upload the CSV to continue!")
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
