# Quick Start Guide

## Cara Cepat Menjalankan Aplikasi

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Jalankan Aplikasi
```bash
python app.py
```

### 3. Buka Browser
Akses aplikasi di: **http://localhost:5000**

---

## Menu yang Tersedia

1. **Home** - Halaman utama dengan deskripsi fitur
2. **Corrosion Calculator** - Hitung laju korosi manual
3. **Fluid Sampling** - Input data sampling
4. **Short Term** - Prediksi ML jangka pendek
5. **Long Term** - Prediksi ML jangka panjang

---

## Test Manual (Tanpa ML Model)

Jika model ML belum tersedia, Anda tetap bisa menggunakan **Corrosion Calculator** untuk perhitungan manual.

### Contoh Input untuk Bottom:
- Equipment: Storage Tank
- Part: Bottom
- Actual Thickness: 10 mm
- Min Thickness: 2.5 mm
- SRB Count: 1000
- Soil Resistivity: 5000

Klik **Calculate** untuk melihat hasil dan grafik proyeksi.

---

## Troubleshooting Cepat

**Error: Port sudah digunakan**
```bash
# Ubah port di app.py line terakhir:
app.run(debug=True, host='0.0.0.0', port=5001)
```

**Error: Module not found**
```bash
pip install flask numpy joblib scikit-learn
```

**Warning: Model tidak ditemukan**
- Ini normal jika file model_str.joblib atau model_ltr.joblib tidak ada
- Corrosion Calculator tetap berfungsi
- Short Term dan Long Term akan menampilkan error saat predict

---

## Screenshot Fitur

### 1. Corrosion Calculator
- Input parameter equipment (bottom/shell/roof)
- Hasil: Corrosion Rate, Remaining Life, Retirement Year
- Grafik proyeksi ketebalan 25 tahun

### 2. Fluid Sampling
- Form input data sampling lengkap
- Tabel data yang tersimpan
- Export ready (untuk pengembangan selanjutnya)

### 3. Short Term Prediction
- Input 5 parameter utama
- Hasil prediksi dengan grafik trend 3 bulan
- Chart impact parameter

### 4. Long Term Prediction  
- Input parameter environment lengkap
- Proyeksi degradasi 10 tahun
- Maintenance schedule recommendation
- Risk assessment chart

---

## Tips Penggunaan

1. **Mulai dari Home** untuk memahami setiap fitur
2. **Gunakan Corrosion Calculator** untuk perhitungan cepat
3. **Input Fluid Sampling** untuk dokumentasi data
4. **Gunakan ML Prediction** jika model sudah tersedia dan terlatih

---

## Next Steps

- Train model ML dengan data Anda sendiri
- Integrasikan database untuk data persistence
- Tambahkan export functionality
- Implementasi user authentication

Selamat mencoba! 🚀
