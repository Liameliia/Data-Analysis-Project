# Memanggil semua library yang dibutuhkan
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency
sns.set(style='dark')

# Mengunggah file data hourly_df dan daily_df
hourly_df = pd.read_csv("Dashboard/hourly_df.csv")
daily_df = pd.read_csv("Dashboard/daily_df.csv")

# Memastikan tipe data pada kolom dteday menjadi datetime pada hourly_df dan daily_df
datetime_columns = ["dteday"]
for column in datetime_columns:
  hourly_df[column] = pd.to_datetime(hourly_df[column])

datetime_columns = ["dteday"]
for column in datetime_columns:
  daily_df[column] = pd.to_datetime(daily_df[column])

with st.sidebar:
    # Menambahkan logo
    st.image("Dashboard/logo.png", width=300)
    
    # Menampilkan informasi umum tentang data
    st.sidebar.header("About Dataset")
    st.sidebar.write("This dataset contains bike usage data by day and hour, including weathersit and season information.")
    
    # Menambahkan grafik kecil di sidebar
    st.sidebar.header("Recent Users Trends")
    # Grafik tren pengguna dalam 7 hari terakhir
    recent_data = daily_df.tail(7)
    st.sidebar.line_chart(recent_data['cnt'])
    

st.title("BIKE USAGE ANALYSIS DASHBOARD")
st.header("Summary Statistics")
st.header("Average Bike Users by Hour")

# Mengelompokkan data berdasarkan jam dan menghitung total serta rata-rata pengguna
hourly_usage = hourly_df.groupby(by='hr').agg({
    'registered' : ['sum', 'mean'],
    'casual' : ['sum', 'mean']
  }).reset_index()

# Menyesuaikan nama kolom
hourly_usage.columns = ['hour', 'registered_total', 'registered_mean', 'casual_total', 'casual_mean']

# Mendapatkan jam dengan jumlah pengguna terdaftar tertinggi dan terendah
max_registered_hour = hourly_usage.loc[hourly_usage['registered_mean'].idxmax(), 'hour']
min_registered_hour = hourly_usage.loc[hourly_usage['registered_mean'].idxmin(), 'hour']

# Mendapatkan jam dengan jumlah pengguna tidak terdaftar tertinggi dan terendah
max_casual_hour = hourly_usage.loc[hourly_usage['casual_mean'].idxmax(), 'hour']
min_casual_hour = hourly_usage.loc[hourly_usage['casual_mean'].idxmin(), 'hour']

st.write(f"**Registered Users:** Peak Time: {max_registered_hour}:00, Low Time: {min_registered_hour}:00")
st.write(f"**Casual Users:** Peak Time: {max_casual_hour}:00, Low Time: {min_casual_hour}:00")

# Membuat line chart terkait Rata-rata Pengguna Sepeda Berdasarkan Jam
fig, ax = plt.subplots(figsize=(10, 5))
ax.plot(hourly_usage['hour'], hourly_usage['registered_mean'], marker='o', label='Registered')
ax.plot(hourly_usage['hour'], hourly_usage['casual_mean'], marker='s', label='Casual')
ax.set_title('Average Bike Users by Hour')
ax.set_xlabel('Hour')
ax.set_ylabel('Average Bike Users')
ax.legend(title='Type of Bike Users')
st.pyplot(fig)

# Membuat bar chart terkait Rata-rata Pengguna Sepeda Berdasarkan Musim dan Kondisi Cuaca
st.header("Average Bike Users by Season and Weathersit")
season_weather_usage = daily_df.groupby(['season', 'weathersit']).agg(
    bike_users=('cnt', 'mean')
).reset_index()
season_weather_usage['bike_users'] = season_weather_usage['bike_users'].round()
season_weather_usage['season'] = season_weather_usage['season'].map({
    1: 'Spring', 2: 'Summer', 3: 'Fall', 4: 'Winter'
})
season_weather_usage['weathersit'] = season_weather_usage['weathersit'].map({
    1: 'Clear', 2: 'Mist/Cloudy', 3: 'Rain/Snow', 4: 'Extreme'
})

fig, ax = plt.subplots(figsize=(10, 5))
sns.barplot(data=season_weather_usage, x='season', y='bike_users', hue='weathersit', palette='coolwarm', ax=ax)
ax.set_title("Average Bike Users by Season and Weather")
ax.set_xlabel("Season")
ax.set_ylabel("Average Bike Users")
st.pyplot(fig)

# Analisis RFM
st.header("RFM Segmentation of Daily Bike Users")
hourly_df = pd.read_csv('hourly_df.csv')  
rfm_df = hourly_df.groupby(by=["dteday"], as_index=False).agg({
    "cnt": ["count", "sum"]
})
rfm_df.columns = ["dteday", "frequency", "monetary"]
rfm_df['dteday'] = pd.to_datetime(rfm_df['dteday'])
recent_date = rfm_df['dteday'].max()
rfm_df["recency"] = rfm_df["dteday"].apply(lambda x: (recent_date - x).days)

fig, ax = plt.subplots(nrows=1, ncols=3, figsize=(30, 6))

colors = ["#1F77B4", "#1F77B4", "#1F77B4", "#1F77B4", "#1F77B4"]

sns.barplot(y="recency", x="dteday", hue="dteday", data=rfm_df.sort_values(by="recency", ascending=True).head(5), palette=colors, ax=ax[0])
ax[0].set_ylabel(None)
ax[0].set_xlabel(None)
ax[0].set_title("By Recency (days)", loc="center", fontsize=18)
ax[0].tick_params(axis ='x', labelsize=15)

sns.barplot(y="frequency", x="dteday", hue="dteday", data=rfm_df.sort_values(by="frequency", ascending=False).head(5), palette=colors, ax=ax[1])
ax[1].set_ylabel(None)
ax[1].set_xlabel(None)
ax[1].set_title("By Frequency", loc="center", fontsize=18)
ax[1].tick_params(axis='x', labelsize=15)

sns.barplot(y="monetary", x="dteday", hue="dteday", data=rfm_df.sort_values(by="monetary", ascending=False).head(5), palette=colors, ax=ax[2])
ax[2].set_ylabel(None)
ax[2].set_xlabel(None)
ax[2].set_title("By Monetary", loc="center", fontsize=18)
ax[2].tick_params(axis='x', labelsize=15)

plt.suptitle("RFM Segmentation of Daily Bike Users", fontsize=20)
st.pyplot(fig)

st.header("Explore Bike Usage Trends")
# Filter untuk memilih musim
season_options = ['Spring', 'Summer', 'Fall', 'Winter']
season_filter = st.selectbox('Select Season:', season_options)

# Filter untuk memilih kondisi cuaca
weather_options = ['Clear', 'Mist/Cloudy', 'Rain/Snow', 'Extreme']
weather_filter = st.multiselect('Select Weathersit:', weather_options, default=weather_options)

# Filter untuk memilih tanggal (tanggal awal dan tanggal akhir)
start_date = st.date_input(
    'Select Start Date:',
    value=pd.to_datetime('01/01/2011'),  # Tanggal default
    min_value=pd.to_datetime('01/01/2011'),  # Tanggal awal dataset
    max_value=pd.to_datetime('31/12/2012')  # Tanggal akhir dataset
)

end_date = st.date_input(
    'Select End Date:',
    value=pd.to_datetime('31/12/2012'),  # Tanggal default
    min_value=pd.to_datetime('01/01/2011'),  # Tanggal awal dataset
    max_value=pd.to_datetime('31/12/2012')  # Tanggal akhir dataset
)

# Mengonversi start_date dan end_date ke dalam format datetime64[ns]
start_date = pd.to_datetime(start_date)
end_date = pd.to_datetime(end_date)

# Menampilkan informasi yang dipilih
st.write(f"Selected Season: {season_filter}")
st.write(f"Selected Date Range: {start_date} - {end_date}")
st.write(f"Selected Weathersit: {', '.join(weather_filter)}")

# Mapping 'season' dan 'weathersit' menggunakan angka
season_map = {
    1: 'Spring',
    2: 'Summer',
    3: 'Fall',
    4: 'Winter'
}
daily_df['season_name'] = daily_df['season'].map(season_map)

weathersit_map = {
    1: 'Clear',
    2: 'Mist/Cloudy',
    3: 'Rain/Snow',
    4: 'Extreme'
}
daily_df['weathersit_name'] = daily_df['weathersit'].map(weathersit_map)

# Filter Dataframe berdasarkan pilihan
filtered_data = daily_df[
    (daily_df['season_name'] == season_filter) &
    (daily_df['dteday'] >= start_date) & (daily_df['dteday'] <= end_date) &
    (daily_df['weathersit_name'].isin(weather_filter))
]

if not filtered_data.empty:
    st.write(f"Displaying {filtered_data.shape[0]} rows of data after filter.")
    fig, ax = plt.subplots(figsize=(10, 5))
    # Mengelompokkan berdasarkan hari dan menghitung rata-rata pengguna
    daily_usage = filtered_data.groupby('dteday').agg({
        'registered': 'sum', 
        'casual': 'sum'
    }).reset_index()

    ax.plot(daily_usage['dteday'], daily_usage['registered'], label='Registered', marker='o', color='blue')
    ax.plot(daily_usage['dteday'], daily_usage['casual'], label='Casual', marker='s', color='orange')

    ax.set_title('Bike Users by Day')
    ax.set_xlabel('Date')
    ax.set_ylabel('Total of Users')
    ax.legend()

    st.pyplot(fig)

else:
    st.write("No data matches the selected filter.")
