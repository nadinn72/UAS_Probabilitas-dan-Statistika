# Langkah 1: Mengimport pustaka Python yang diperlukan
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Langkah 2: Membuat DataFrame
dataframe = pd.read_csv("Zomato-data-.csv")
print("DataFrame Awal:")
print(dataframe.head())
print("\n")

# Langkah 3: Pembersihan dan Persiapan Data
# 1. Konversi kolom rate menjadi float
def handleRate(value):
    if isinstance(value, str) and '/' in value:
        value = str(value).split('/')[0]
    try:
        return float(value)
    except:
        return np.nan

dataframe['rate'] = dataframe['rate'].apply(handleRate)

print("DataFrame setelah konversi rate:")
print(dataframe.head())
print("\n")

# 2. Ringkasan DataFrame
print("Info DataFrame:")
dataframe.info()
print("\n")

# 3. Memeriksa nilai yang hilang
print("Jumlah nilai null per kolom:")
print(dataframe.isnull().sum())
print("\n")

# Langkah 4: Menjelajahi Jenis Restoran
# 1. Countplot untuk jenis restoran
plt.figure(figsize=(10,6))
sns.countplot(x=dataframe['listed_in(type)'])
plt.xlabel("Type of restaurant")
plt.title("Distribusi Jenis Restoran")
plt.xticks(rotation=45)
plt.show()

# 2. Informasi berdasarkan jenis restoran (total votes per jenis)
grouped_data = dataframe.groupby('listed_in(type)')['votes'].sum()
result = pd.DataFrame({'votes': grouped_data})
plt.figure(figsize=(10,6))
plt.plot(result.index, result['votes'], c='green', marker='o')
plt.xlabel('Type of restaurant')
plt.ylabel('Total Votes')
plt.title('Total Votes per Jenis Restoran')
plt.xticks(rotation=45)
plt.grid(True)
plt.show()

# Langkah 5: Identifikasi Restoran yang Paling Banyak Dipilih
max_votes = dataframe['votes'].max()
restaurant_with_max_votes = dataframe.loc[dataframe['votes'] == max_votes, 'name']

print('Restaurant(s) with the maximum votes:')
print(restaurant_with_max_votes)
print("\n")

# Langkah 6: Ketersediaan Pesanan Online
plt.figure(figsize=(6,4))
sns.countplot(x=dataframe['online_order'])
plt.title('Ketersediaan Pesanan Online')
plt.xlabel('Online Order')
plt.ylabel('Count')
plt.show()

# Langkah 7: Analisis Peringkat (Distribusi Rating)
plt.figure(figsize=(8,5))
plt.hist(dataframe['rate'].dropna(), bins=20, edgecolor='black')
plt.title('Distribusi Rating Restoran')
plt.xlabel('Rating')
plt.ylabel('Frekuensi')
plt.grid(True)
plt.show()

# Langkah 8: Perkiraan Biaya untuk Pasangan
plt.figure(figsize=(10,6))
sns.countplot(x=dataframe['approx_cost(for two people)'])
plt.title('Distribusi Perkiraan Biaya untuk Dua Orang')
plt.xlabel('Approx Cost (for two people)')
plt.ylabel('Count')
plt.xticks(rotation=90)
plt.show()

# Langkah 9: Perbandingan Peringkat - Pesanan Online vs Offline
plt.figure(figsize=(8,6))
sns.boxplot(x='online_order', y='rate', data=dataframe)
plt.title('Perbandingan Rating: Pesanan Online vs Offline')
plt.xlabel('Online Order')
plt.ylabel('Rating')
plt.show()

# Langkah 10: Preferensi Mode Pesanan berdasarkan Jenis Restoran
pivot_table = dataframe.pivot_table(index='listed_in(type)', 
                                columns='online_order', 
                                aggfunc='size', 
                                fill_value=0)

plt.figure(figsize=(10,6))
sns.heatmap(pivot_table, annot=True, cmap='YlGnBu', fmt='d')
plt.title('Heatmap: Hubungan Jenis Restoran dan Pesanan Online')
plt.xlabel('Online Order')
plt.ylabel('Listed In (Type)')
plt.tight_layout()
plt.show()

# Analisis tambahan: Statistik deskriptif
print("\nStatistik Deskriptif:")
print(dataframe.describe())

# Analisis korelasi antara rating dan biaya
print("\nKorelasi antara Rating dan Biaya untuk Dua Orang:")
correlation = dataframe['rate'].corr(dataframe['approx_cost(for two people)'])
print(f"Korelasi: {correlation:.3f}")