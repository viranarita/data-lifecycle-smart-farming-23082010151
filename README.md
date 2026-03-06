Ini dia file `README.md` yang sudah diperbaiki bagian *bash code blocks* dan format keseluruhannya agar terlihat profesional di GitHub. Kamu tinggal salin teks di dalam kotak di bawah ini:

---

```markdown
# 🌿 Data Lifecycle Smart Farming Dashboard

Proyek ini adalah implementasi siklus hidup data (*Data Lifecycle*) terpadu untuk sistem pertanian cerdas (*Smart Farming*). Repositori ini mencakup seluruh tahapan mulai dari ekstraksi data mentah via Kaggle API, pembersihan data (*data cleaning* & penanganan *outliers*), hingga penyajian wawasan melalui *dashboard* interaktif yang memantau kondisi lahan secara *real-time*.

## 📊 Evaluasi Kualitas Data & Key Insights

Sebelum divisualisasikan, dataset yang berisi 500 observasi sensor telah melalui tahap evaluasi kualitas data yang ketat:

* **Accuracy Score**: **97.45%** (Dihitung dengan rumus $1 - (\text{missing}/\text{total})$) [cite: 81-82, 85, 96].
* **Completeness Score**: **97.45%** (Dihitung dengan rumus $\text{non-null}/\text{total}$, tidak ada *missing values* pada kolom metrik utama).
* **Timeliness Score**: **1.40%** (Persentase data yang tercatat dalam 30 hari terakhir dari total dataset).

**Insight Temuan Utama:**
* Rata-rata **Kelembapan Tanah** berada di **26.75%** (kering namun masih di atas batas kritis).
* Rata-rata **pH Tanah** berada di **6.52** (tingkat keasaman yang sangat optimal untuk hasil panen).

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
└── README.md

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
