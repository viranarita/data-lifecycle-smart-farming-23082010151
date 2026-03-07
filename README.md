
# 🌿 Data Lifecycle Smart Farming Dashboard 🌿

Proyek ini adalah implementasi siklus hidup data (*Data Lifecycle*) terpadu untuk sistem pertanian cerdas (*Smart Farming*). Repositori ini mencakup seluruh tahapan mulai dari ekstraksi data mentah via Kaggle API, pembersihan data (*data cleaning* & penanganan *outliers*), hingga penyajian wawasan melalui *dashboard* interaktif yang memantau kondisi lahan secara *real-time*.

## 📊 Evaluasi Kualitas Data & Key Insights

Sebelum divisualisasikan, dataset yang berisi 500 observasi sensor telah melalui tahap evaluasi kualitas data yang ketat:

* **Accuracy Score**: **97.45%** 
* **Completeness Score**: **97.45%** 
* **Timeliness Score**: **1.40%** 

**Insight Temuan Utama:**
* **Kondisi Lahan**: Lahan secara keseluruhan berada dalam status sehat.
* **Suhu**: Suhu rata-rata berada di kisaran **25°C**, ideal untuk pertumbuhan tanaman.
* **Kelembaban Tanah**: Kelembaban tanah rata-rata berada di kisaran **45%**, menunjukkan kondisi tanah yang cukup lembab.
* **Kelembaban Udara**: Kelembaban udara rata-rata berada di kisaran **60%**, menunjukkan kondisi udara yang cukup lembab.
* **pH Tanah**: pH tanah rata-rata berada di kisaran **6.5**, menunjukkan kondisi tanah yang relatif stabil.
* **NDVI**: NDVI rata-rata berada di kisaran **0.75**, menunjukkan kesehatan tanaman yang baik.
* **Hasil Panen**: Hasil panen rata-rata berada di kisaran **5000 kg/hektar**, menunjukkan hasil panen yang baik.

## ✨ Fitur Utama Dashboard

Dashboard Streamlit ini dirancang untuk memberikan peringatan dini dan analisis mendalam:
* 📅 **Global Filters**: Pemfilteran dinamis berdasarkan rentang waktu dan resolusi agregasi data (Harian, Mingguan, Bulanan) yang otomatis mengontrol seluruh visualisasi.
* 🚨 **Smart Alert System**: Indikator warna otomatis (Merah/Hijau) yang mendeteksi anomali. Akan menyala merah jika kelembapan tanah anjlok < 20% (butuh irigasi) atau indeks NDVI < 0.3 (kesehatan tanaman memburuk).
* 🧭 **Soil Moisture Gauge Meter**: Indikator persentase kelembapan tanah aktual dengan batas zona kritis, optimal, dan terlalu basah.
* 📈 **Sensor Trend Analysis**: Visualisasi deret waktu (*line chart*) untuk melacak fluktuasi Suhu, Kelembapan Tanah, Kelembapan Udara, dan pH.
* 🗺️ **Correlation Heatmap**: Matriks korelasi antar variabel sensor untuk melihat hubungan fitur terhadap hasil panen (*yield*).

## 📁 Struktur Direktori

Proyek ini disusun dengan standar arsitektur direktori analitik sebagai berikut:

```text
.
├── .streamlit/
│   └── config.toml                          
├── dashboard/
│   └── streamlit_app.py                    
├── data/
│   └── raw/
│       └── Smart_Farming_Crop_Yield_2024.csv 
├── outputs/
│   ├── cleaned_data.csv                     
│   ├── analysis_report.pdf                 
│   └── dashboard_screenshot.png            
├── Data_Lifecycle_Smart_Farming.ipynb
├── README.md
└── requirements.txt

```

## 🚀 Cara Instalasi & Menjalankan Aplikasi

Pastikan Python sudah terinstal di sistem Anda. Ikuti langkah-langkah berikut untuk menjalankan dashboard secara lokal:

1. **Clone repositori ini:**
```bash
git clone https://github.com/viranarita/data-lifecycle-smart-farming-23082010151.git
cd data-lifecycle-smart-farming-23082010151
```

2. **Instal seluruh dependensi library:**
```bash
pip install -r requirements.txt

```

*(Library utama: pandas, streamlit, plotly, matplotlib, seaborn, kagglehub)*

3. **Jalankan Dashboard Streamlit:**
> ⚠️ **Penting:** Pastikan Anda mengeksekusi perintah ini langsung dari folder utama proyek (*root directory*), bukan dari dalam folder dashboard.


```bash
streamlit run dashboard/streamlit_app.py

```

## 🛠️ Tech Stack

* **Analisis Data**: Python, Pandas, Matplotlib, Seaborn.
* **Pengambilan Data**: Kagglehub API.
* **Visualisasi Dashboard**: Streamlit, Plotly Express & Plotly Graph Objects.
