# Aplikasi Kalkulator Corrosion Rate

Aplikasi web berbasis Flask untuk menghitung dan memprediksi laju korosi pada equipment industri dengan 4 menu utama:
1. **Corrosion Rate Calculator** - Perhitungan laju korosi berdasarkan parameter equipment
2. **Fluid Sampling** - Input dan manajemen data sampling fluida
3. **Short Term Prediction** - Prediksi laju korosi jangka pendek (1-3 bulan)
4. **Long Term Prediction** - Prediksi laju korosi jangka panjang (1-10 tahun)

## Fitur Utama

### 1. Corrosion Rate Calculator
- Perhitungan laju korosi untuk berbagai tipe equipment (Storage Tank, Pressure Vessel, Heat Exchanger, dll)
- Parameter spesifik untuk Bottom, Shell, dan Roof
- Visualisasi grafik proyeksi ketebalan
- Estimasi remaining life dan retirement year

### 2. Fluid Sampling
- Input data sampling fluida dengan parameter lengkap (pH, temperature, chloride, dll)
- Manajemen data sampling (tambah, lihat, hapus)
- Storage data untuk analisis lebih lanjut

### 3. Short Term Prediction
- Prediksi menggunakan machine learning model
- Parameter: pH, temperature, chloride, oxygen, flow rate
- Visualisasi trend 3 bulan ke depan
- Analisis impact parameter terhadap laju korosi

### 4. Long Term Prediction
- Prediksi jangka panjang untuk perencanaan maintenance
- Proyeksi degradasi ketebalan 10 tahun
- Jadwal maintenance yang direkomendasikan
- Risk assessment

## Instalasi

### Prerequisites
- Python 3.7 atau lebih tinggi
- pip (Python package manager)

### Langkah Instalasi

1. Clone atau download repository ini

2. Install dependencies:
```bash
pip install flask numpy joblib scikit-learn pandas
```

3. Pastikan file model ML ada di direktori yang sama:
   - `model_str.joblib` (Short-term model)
   - `model_ltr.joblib` (Long-term model)

## Cara Menjalankan

1. Jalankan aplikasi Flask:
```bash
python app.py
```

2. Buka browser dan akses:
```
http://localhost:5000
```

3. Aplikasi akan berjalan di port 5000 secara default

## Struktur Folder

```
kalkulator-CR/
│
├── app.py                          # Main Flask application
├── model_str.joblib                # Short-term ML model
├── model_ltr.joblib                # Long-term ML model
├── README.md                       # Dokumentasi
│
├── templates/                      # HTML templates
│   ├── index.html                 # Homepage
│   ├── corrosion_calculator.html  # Corrosion calculator page
│   ├── fluid_sampling.html        # Fluid sampling page
│   ├── short_term.html            # Short-term prediction page
│   └── long_term.html             # Long-term prediction page
│
└── static/                         # Static files
    └── style.css                  # CSS styling
```

## API Endpoints

### 1. Calculate Corrosion Rate
```
POST /api/calculate-corrosion
Content-Type: application/json

Body:
{
    "part": "bottom",
    "actual_thickness": 10.0,
    "min_thickness": 2.5,
    "year": 2024,
    "soil_resistivity": 5000,
    "srb_count": 1000
}

Response:
{
    "success": true,
    "corrosion_rate": 1.200,
    "remaining_life": 6.3,
    "retirement_year": 2030
}
```

### 2. Predict Short Term
```
POST /api/predict-short-term
Content-Type: application/json

Body:
{
    "pH": 7.0,
    "temperature": 25.0,
    "chloride": 100.0,
    "oxygen": 5.0,
    "flow_rate": 1.0
}

Response:
{
    "success": true,
    "predicted_corrosion_rate": 0.145
}
```

### 3. Predict Long Term
```
POST /api/predict-long-term
Content-Type: application/json

Body:
{
    "pH": 7.0,
    "temperature": 25.0,
    "chloride": 100.0,
    "sulfate": 50.0,
    "hardness": 200.0,
    "alkalinity": 100.0
}

Response:
{
    "success": true,
    "predicted_corrosion_rate": 0.125
}
```

### 4. Save Fluid Sample
```
POST /api/save-fluid-sample
Content-Type: application/json

Body:
{
    "sample_id": "FS-2024-001",
    "sample_date": "2024-01-15",
    "location": "Tank-101",
    "pH": 7.0,
    "temperature": 25.0,
    ...
}

Response:
{
    "success": true,
    "message": "Data sampling berhasil disimpan",
    "sample_id": "FS-2024-001"
}
```

## Teknologi yang Digunakan

- **Backend**: Flask (Python)
- **Frontend**: HTML5, CSS3, JavaScript
- **Charting**: Chart.js
- **Machine Learning**: scikit-learn, joblib
- **Data Processing**: NumPy, Pandas

## Catatan Penting

1. **Model ML**: Aplikasi memerlukan file model ML (`model_str.joblib` dan `model_ltr.joblib`). Jika model tidak ditemukan, fungsi prediksi ML tidak akan berfungsi, tetapi kalkulator manual tetap dapat digunakan.

2. **Data Storage**: Saat ini data fluid sampling disimpan dalam memory (akan hilang saat server restart). Untuk production, disarankan menggunakan database (SQLite, PostgreSQL, dll).

3. **Parameter Model**: Feature yang digunakan dalam model ML perlu disesuaikan dengan model yang sebenarnya digunakan. Sesuaikan di fungsi `predict_short_term()` dan `predict_long_term()` di `app.py`.

## Pengembangan Lebih Lanjut

Beberapa fitur yang bisa ditambahkan:
- Database integration untuk persistent storage
- Export data ke Excel/PDF
- User authentication dan authorization
- Historical data analysis
- Email notifications untuk maintenance schedule
- Dashboard analytics
- Multi-language support

## Troubleshooting

### Model tidak ditemukan
Jika muncul pesan "Model belum dimuat", pastikan file model ML ada di direktori yang sama dengan `app.py`.

### Port sudah digunakan
Jika port 5000 sudah digunakan, ubah di `app.py`:
```python
app.run(debug=True, host='0.0.0.0', port=5001)
```

### Import Error
Pastikan semua dependencies terinstall:
```bash
pip install -r requirements.txt
```

## Lisensi

Project ini dibuat untuk keperluan internal dan edukasi.

## Kontak

Untuk pertanyaan atau support, silakan hubungi tim development.
