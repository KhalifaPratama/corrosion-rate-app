# 📚 Panduan Lengkap Aplikasi Kalkulator Corrosion Rate

## 🎯 Deskripsi Aplikasi

Aplikasi web komprehensif untuk analisis dan prediksi laju korosi pada equipment industri dengan 4 menu utama yang terintegrasi.

---

## 🌟 Fitur Utama

### 1. 🧮 Corrosion Rate Calculator
**Tujuan:** Perhitungan laju korosi manual berdasarkan parameter fisik dan kimia

**Parameter Input:**
- **Equipment Type:** Storage Tank, Pressure Vessel, Heat Exchanger, Fin Fan Cooler, Stack
- **Part Selection:** Bottom, Shell, Roof
- **Inspection Year:** Tahun inspeksi
- **Actual Thickness:** Ketebalan saat ini (mm)
- **Minimal Thickness:** Ketebalan minimal yang diizinkan (mm)

**Parameter Spesifik per Part:**

**Bottom:**
- SRB Count (Sulfate Reducing Bacteria)
- Soil Resistivity (Ω-cm)
- Kandungan Klorida (ppm)

**Shell:**
- pH
- Operating Temperature (°C)
- Water Content (%)

**Roof:**
- H2S Concentration (ppm)
- CO2 Concentration (%)
- Humidity Level (%)

**Output:**
- Corrosion Rate (mm/year)
- Remaining Life (years)
- Retirement Year (estimasi)
- Grafik proyeksi ketebalan 25 tahun

---

### 2. 🔬 Fluid Sampling

**Tujuan:** Input dan manajemen data sampling fluida untuk dokumentasi

**Data yang Diinput:**

**Informasi Dasar:**
- Sample ID (unik)
- Tanggal Sampling
- Lokasi Sampling
- Equipment Type

**Parameter Kimia:**
- pH (0-14)
- Temperature (°C)
- Chloride (ppm)
- Sulfate (ppm)
- Dissolved Oxygen (ppm)
- CO2 Content (%)
- H2S Content (ppm)
- Total Hardness (ppm as CaCO3)
- Total Alkalinity (ppm as CaCO3)
- Conductivity (µS/cm)
- Iron Content (ppm)
- Water Content (%)

**Parameter Operasi:**
- Flow Rate (m/s)
- Pressure (bar)
- SRB Count (cells/mL)
- Catatan tambahan

**Fungsi:**
- Menyimpan data sampling
- Menampilkan tabel data tersimpan
- Menghapus data
- Data dapat digunakan untuk prediksi ML

---

### 3. ⏱️ Short Term Prediction

**Tujuan:** Prediksi laju korosi jangka pendek (1-3 bulan) menggunakan Machine Learning

**Kapan Digunakan:**
- Monitoring kondisi operasi saat ini
- Troubleshooting masalah korosi
- Evaluasi cepat setelah perubahan kondisi operasi

**Parameter Input:**
- pH
- Temperature (°C)
- Chloride Content (ppm)
- Dissolved Oxygen (ppm)
- Flow Rate (m/s)

**Output:**
- Predicted Corrosion Rate (mm/year)
- Classification (Low/Medium/High)
- Recommended Action
- Grafik trend 3 bulan
- Parameter Impact Chart

**Klasifikasi:**
- **Low** (< 0.1 mm/year): Normal Monitoring
- **Medium** (0.1-0.5 mm/year): Increased Monitoring
- **High** (> 0.5 mm/year): Immediate Action Required

---

### 4. 📈 Long Term Prediction

**Tujuan:** Prediksi laju korosi jangka panjang (1-10 tahun) untuk perencanaan maintenance

**Kapan Digunakan:**
- Perencanaan maintenance jangka panjang
- Estimasi umur equipment
- Budget planning untuk replacement
- Risk assessment

**Parameter Input:**

**Equipment Info:**
- Equipment ID
- Current Thickness (mm)
- Minimum Required Thickness (mm)
- Installation Year

**Environmental Parameters:**
- pH (long-term average)
- Average Temperature (°C)
- Chloride Content (ppm)
- Sulfate Content (ppm)
- Total Hardness (ppm)
- Total Alkalinity (ppm)

**Output:**
- Predicted Corrosion Rate (mm/year)
- Estimated Remaining Life (years)
- Retirement Year
- 10-Year Thickness Degradation Chart
- Recommended Maintenance Schedule
- Risk Assessment Distribution

**Maintenance Schedule:**
- Baseline Inspection
- Regular Inspection (interval otomatis)
- Major Inspection
- Timeline visual

---

## 🚀 Instalasi dan Setup

### Metode 1: Menggunakan Batch File (Recommended untuk Windows)

1. **Install Dependencies:**
   ```
   Double-click: install.bat
   ```

2. **Jalankan Aplikasi:**
   ```
   Double-click: run.bat
   ```

3. **Buka Browser:**
   ```
   http://localhost:5000
   ```

### Metode 2: Manual via Command Line

1. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Jalankan Aplikasi:**
   ```bash
   python app.py
   ```

3. **Buka Browser:**
   ```
   http://localhost:5000
   ```

---

## 📖 Cara Penggunaan

### Skenario 1: Perhitungan Corrosion Rate Manual

1. Buka menu **Corrosion Calculator**
2. Pilih Equipment Type (e.g., Storage Tank)
3. Pilih Part yang ingin dianalisis (Bottom/Shell/Roof)
4. Input parameter yang diminta
5. Klik **Calculate Corrosion Rate**
6. Lihat hasil dan grafik proyeksi

**Contoh Input (Bottom):**
- Equipment: Storage Tank
- Part: Bottom
- Inspection Year: 2024
- Actual Thickness: 10 mm
- Min Thickness: 2.5 mm
- SRB Count: 1000
- Soil Resistivity: 5000 Ω-cm

**Hasil:**
- Corrosion Rate: 1.200 mm/year
- Remaining Life: 6.3 years
- Retirement Year: 2030

---

### Skenario 2: Input Data Sampling

1. Buka menu **Fluid Sampling**
2. Isi informasi sampling (Sample ID, Tanggal, Lokasi)
3. Isi parameter kimia sesuai hasil lab
4. Isi parameter operasi
5. Tambahkan catatan jika perlu
6. Klik **Simpan Data Sampling**
7. Data akan muncul di tabel bawah

**Tips:**
- Gunakan format Sample ID yang konsisten (e.g., FS-2024-001)
- Data tersimpan selama server berjalan
- Export functionality akan ditambahkan di versi selanjutnya

---

### Skenario 3: Prediksi Short Term

1. Buka menu **Short Term**
2. Input parameter operasi saat ini:
   - pH: 7.0
   - Temperature: 25°C
   - Chloride: 100 ppm
   - Oxygen: 5 ppm
   - Flow Rate: 1.0 m/s
3. Klik **Predict Corrosion Rate**
4. Lihat hasil prediksi dan klasifikasi
5. Analisis parameter impact chart
6. Follow recommended action

**Catatan:** Memerlukan file model_str.joblib

---

### Skenario 4: Prediksi Long Term

1. Buka menu **Long Term**
2. Isi Equipment Information
3. Isi Environmental Parameters (rata-rata jangka panjang)
4. Klik **Predict Long Term Behavior**
5. Review predicted corrosion rate dan remaining life
6. Lihat 10-year degradation chart
7. Catat maintenance schedule yang direkomendasikan
8. Review risk assessment

**Catatan:** Memerlukan file model_ltr.joblib

---

## 🔧 Konfigurasi

### Mengubah Port Server

Edit file `app.py` di bagian paling bawah:

```python
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)  # Ubah port di sini
```

### Mengaktifkan/Menonaktifkan Debug Mode

```python
app.run(debug=False, host='0.0.0.0', port=5000)  # Set debug=False untuk production
```

---

## 🎨 Customization

### Mengubah Warna Theme

Edit file `static/style.css`:

```css
/* Gradient utama */
background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);

/* Ubah sesuai selera, contoh: */
background: linear-gradient(135deg, #ff6b6b 0%, #4ecdc4 100%);
```

### Menambahkan Equipment Type Baru

Edit file `templates/corrosion_calculator.html`:

```html
<select id="equipmentSelector">
    <option value="ST">Storage Tank</option>
    <option value="PV">Pressure Vessel</option>
    <!-- Tambahkan di sini -->
    <option value="PIPE">Pipeline</option>
</select>
```

---

## 🧪 Testing

### Test Corrosion Calculator

**Test Case 1: Bottom Corrosion**
- Input: SRB=1000, Soil Res=5000
- Expected CR: ~1.2 mm/year

**Test Case 2: Shell Corrosion**
- Input: Temp=40°C, Water=0.5%
- Expected CR: ~0.25 mm/year

**Test Case 3: Roof Corrosion**
- Input: H2S=10ppm, Humidity=80%
- Expected CR: ~0.30 mm/year

### Test API Endpoints

Gunakan Postman atau curl:

```bash
curl -X POST http://localhost:5000/api/calculate-corrosion \
  -H "Content-Type: application/json" \
  -d '{
    "part": "bottom",
    "actual_thickness": 10.0,
    "min_thickness": 2.5,
    "year": 2024,
    "soil_resistivity": 5000,
    "srb_count": 1000
  }'
```

---

## ❗ Troubleshooting

### Problem: Model tidak ditemukan

**Solusi:**
- Pastikan file `model_str.joblib` dan `model_ltr.joblib` ada
- Jika tidak ada, train model dari notebook yang tersedia
- Atau gunakan hanya Corrosion Calculator (tidak perlu model)

### Problem: Port already in use

**Solusi:**
```bash
# Cari process yang menggunakan port 5000
netstat -ano | findstr :5000

# Kill process
taskkill /PID <PID_NUMBER> /F

# Atau ubah port di app.py
```

### Problem: Module not found

**Solusi:**
```bash
# Install ulang dependencies
pip install -r requirements.txt

# Atau install manual
pip install flask numpy joblib scikit-learn pandas
```

### Problem: Browser tidak bisa akses

**Solusi:**
- Check firewall settings
- Pastikan server running (lihat terminal)
- Coba akses: http://127.0.0.1:5000
- Clear browser cache

---

## 📊 Database Integration (Future)

Untuk production, disarankan menambahkan database:

```python
# Contoh dengan SQLite
import sqlite3

def save_sample_to_db(data):
    conn = sqlite3.connect('corrosion_data.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO samples (sample_id, date, location, pH, temperature)
        VALUES (?, ?, ?, ?, ?)
    ''', (data['sample_id'], data['date'], data['location'], 
          data['pH'], data['temperature']))
    conn.commit()
    conn.close()
```

---

## 🔐 Security Considerations

**Untuk Production:**

1. **Disable Debug Mode:**
   ```python
   app.run(debug=False)
   ```

2. **Add Authentication:**
   ```python
   from flask_login import LoginManager, login_required
   ```

3. **Input Validation:**
   - Sudah ada basic validation
   - Tambahkan sanitization untuk production

4. **HTTPS:**
   - Deploy dengan HTTPS/SSL
   - Gunakan reverse proxy (nginx/apache)

---

## 📈 Performance Tips

1. **Caching:** Implement caching untuk hasil prediksi
2. **Database Connection Pool:** Untuk multiple users
3. **Async Processing:** Untuk prediksi ML yang berat
4. **CDN:** Untuk static files (Chart.js, CSS)

---

## 🚀 Deployment

### Deploy ke Cloud (Contoh: Heroku)

1. Buat `Procfile`:
   ```
   web: gunicorn app:app
   ```

2. Install gunicorn:
   ```bash
   pip install gunicorn
   pip freeze > requirements.txt
   ```

3. Deploy:
   ```bash
   heroku create corrosion-rate-app
   git push heroku main
   ```

---

## 📝 API Documentation

Lengkap tersedia di file `README.md`

---

## 🆘 Support

Untuk bantuan lebih lanjut:
1. Baca dokumentasi lengkap
2. Check troubleshooting section
3. Review code comments
4. Hubungi tim development

---

## 📄 Lisensi

Internal use only - Educational purposes

---

## 🎓 Learning Resources

- Flask Documentation: https://flask.palletsprojects.com/
- Chart.js: https://www.chartjs.org/
- Scikit-learn: https://scikit-learn.org/

---

**Selamat menggunakan Aplikasi Kalkulator Corrosion Rate! 🎉**
