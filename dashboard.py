import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import streamlit as st
from babel.numbers import format_currency

# Load data
file_path = "bike.csv"
bike_sharing_df = pd.read_csv(file_path)

# Konversi kolom 'dteday' menjadi tipe datetime
bike_sharing_df['dteday'] = pd.to_datetime(bike_sharing_df['dteday'])

sns.set(style='dark')

# Filter data
min_date = bike_sharing_df["dteday"].min()
max_date = bike_sharing_df["dteday"].max()

with st.sidebar:

    # Mengambil start_date & end_date dari date_input
    start_date, end_date = st.date_input(
        label='Rentang Waktu', min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

# Filter data berdasarkan rentang waktu
main_df = bike_sharing_df[(bike_sharing_df["dteday"] >= str(start_date)) & 
                          (bike_sharing_df["dteday"] <= str(end_date))]

# Ekstrak tahun dan bulan
main_df['yr'] = main_df['dteday'].dt.year
main_df['mnth'] = main_df['dteday'].dt.to_period('M').astype(str)
monthly = main_df.groupby(['yr', 'mnth'])['cnt'].sum().reset_index()

rentals = {year: monthly[monthly['yr'] == year] for year in [2011, 2012]}

st.header('Proyek Data Analisis')
st.subheader('Bike Sharing Dashboard')

# Boxplot Season vs Count
plt.figure(figsize=(10, 5))
sns.boxplot(x='season', y='cnt', data=main_df, hue='season', palette='coolwarm')
plt.title('Pengaruh Musim terhadap Jumlah Penyewaan Sepeda')
st.pyplot(plt)

# Boxplot Weather Situation vs Count
plt.figure(figsize=(10, 5))
sns.boxplot(x='weathersit', y='cnt', data=main_df, hue='weathersit', palette='coolwarm')
plt.title('Pengaruh Cuaca terhadap Jumlah Penyewaan Sepeda')
st.pyplot(plt)

# Plot line chart
plt.figure(figsize=(12, 5))
for year, color, marker in zip([2011, 2012], ['b', 'r'], ['o', 's']):
    plt.plot(rentals[year]['mnth'], rentals[year]['cnt'], marker=marker, linestyle='-', color=color, linewidth=2, label=str(year))

plt.xticks(rotation=45)
plt.title('Tren Penyewaan Sepeda dalam 2 Tahun Terakhir', fontsize=14)
plt.xlabel('Month', fontsize=12)
plt.ylabel('Jumlah Penyewaan', fontsize=12)
plt.legend(title='Year', fontsize=10)
plt.grid(True, linestyle='--', alpha=0.6)
st.pyplot(plt)
