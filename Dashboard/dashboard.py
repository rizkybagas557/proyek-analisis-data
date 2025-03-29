import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import streamlit as st

# Membaca data gabungan
all_df = pd.read_csv("Dashboard/all_data.csv")

# Sidebar untuk memilih stasiun
st.sidebar.title("Filter Data")
station_filter = st.sidebar.selectbox("Pilih Stasiun:", all_df["station"].unique())

# Filter data berdasarkan stasiun yang dipilih
filtered_data = all_df[all_df["station"] == station_filter]

# Judul Dashboard
st.title("Dashboard Analisis Kualitas Udara")
st.subheader(f"Data untuk Stasiun: {station_filter}")

# Matriks Korelasi
st.subheader("Matriks Korelasi Polutan")
correlation = filtered_data[["PM2.5", "PM10", "SO2", "NO2", "CO", "O3", "WSPM"]].corr()

# Visualisasi Matriks Korelasi
fig, ax = plt.subplots(figsize=(8, 6))
sns.heatmap(correlation, annot=True, cmap="coolwarm", fmt=".2f", linewidths=0.5, ax=ax)
st.pyplot(fig)

# Hubungan antara WSPM dan Polutan
st.subheader("Hubungan antara Kecepatan Angin (WSPM) dan Polutan")
pollutant = st.selectbox("Pilih Polutan:", ["PM2.5", "PM10", "SO2", "NO2", "CO", "O3"])

fig, ax = plt.subplots(figsize=(8, 6))
sns.regplot(
    x="WSPM",
    y=pollutant,
    data=filtered_data,
    scatter_kws={"alpha": 0.5},
    line_kws={"color": "red"},
    ax=ax,
)
ax.set_title(f"Hubungan antara WSPM dan {pollutant}")
ax.set_xlabel("Kecepatan Angin (WSPM)")
ax.set_ylabel(f"Konsentrasi {pollutant}")
st.pyplot(fig)

# Rata-rata Konsentrasi Polutan
st.subheader("Rata-Rata Konsentrasi Polutan")
average_pollutants = filtered_data[["PM2.5", "PM10", "SO2", "NO2", "CO", "O3"]].mean()

st.bar_chart(average_pollutants)

# Analisis Berdasarkan Waktu
st.subheader("Analisis Berdasarkan Waktu")
time_filter = st.selectbox("Pilih Analisis Waktu:", ["Year", "Month", "Day", "Hour"])

# Agregasi data berdasarkan waktu
if time_filter == "Year":
    time_data = filtered_data.groupby("year")[
        ["PM2.5", "PM10", "SO2", "NO2", "CO", "O3"]
    ].mean()
elif time_filter == "Month":
    time_data = filtered_data.groupby("month")[
        ["PM2.5", "PM10", "SO2", "NO2", "CO", "O3"]
    ].mean()
elif time_filter == "Day":
    time_data = filtered_data.groupby("day")[
        ["PM2.5", "PM10", "SO2", "NO2", "CO", "O3"]
    ].mean()
elif time_filter == "Hour":
    time_data = filtered_data.groupby("hour")[
        ["PM2.5", "PM10", "SO2", "NO2", "CO", "O3"]
    ].mean()

# Visualisasi data berdasarkan waktu
st.line_chart(time_data)
