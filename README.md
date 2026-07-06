# 🔧 Corrosion Rate Prediction Application

Web application untuk prediksi dan kalkulasi laju korosi menggunakan Machine Learning. Aplikasi ini mendukung 4 metode prediksi berbeda untuk analisis korosi pada peralatan industri.

![Version](https://img.shields.io/badge/version-2.0.1-blue.svg)
![Python](https://img.shields.io/badge/python-3.8+-green.svg)
![Flask](https://img.shields.io/badge/flask-3.1.0-lightgrey.svg)
![License](https://img.shields.io/badge/license-MIT-orange.svg)

---

## ✨ Features

### 1. 🔧 Corrosion Calculator
Manual calculation berbasis formula untuk kalkulasi laju korosi berdasarkan parameter equipment.

**Input:**
- Part type (Bottom/Shell/Roof)
- Actual thickness
- Minimum thickness
- Additional parameters per part type

**Output:**
- Corrosion rate (mm/year)
- Remaining life (years)
- Retirement year

---

### 2. 🧪 Fluid Sampling
ML-based prediction menggunakan 10 parameter fluida kimia.

**Model:** `corrosion-rate.pkl`

**Input (13 fields):**
- Equipment info: Equipment Type, Part, Operating Unit
- Fluid parameters: Cation Anion Balance, HCO₃, Density, Resistivity, pH, Salinity, SO₄, Ca, Mg, Acetic Acid

**Output:**
- Predicted corrosion rate
- Classification (Very Low → Very High)
- Recommendations
- Chart visualization

---

### 3. 📊 Short Term Prediction
ML prediction untuk laju korosi jangka pendek (1-3 bulan).

**Model:** `model_str.joblib`

**Input:**
- Equipment Type
- Part
- Operating Unit (OU)

**Output:** Predicted corrosion rate

---

### 4. 📈 Long Term Prediction
ML prediction untuk laju korosi jangka panjang (1-10 tahun).

**Model:** `model_ltr.joblib`

**Input:**
- Equipment Type
- Part
- Operating Unit (OU)

**Output:** Predicted corrosion rate

---

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Installation

1. **Clone repository:**
   ```bash
   git clone https://github.com/yourusername/corrosion-rate-app.git
   cd corrosion-rate-app
   ```

2. **Create virtual environment:**
   ```bash
   # Windows
   python -m venv venv
   .\venv\Scripts\activate

   # Linux/Mac
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run application:**
   ```bash
   # Development mode
   python app.py

   # Production mode (Windows)
   pip install waitress
   waitress-serve --host=0.0.0.0 --port=5000 wsgi:app

   # Production mode (Linux)
   pip install gunicorn
   gunicorn -w 4 -b 0.0.0.0:5000 wsgi:app
   ```

5. **Open browser:**
   ```
   http://localhost:5000
   ```

---

## 📁 Project Structure

```
corrosion-rate-app/
├── app.py                      # Main Flask application
├── wsgi.py                     # WSGI entry point
├── requirements.txt            # Python dependencies
│
├── models/
│   ├── corrosion-rate.pkl     # Fluid sampling model
│   ├── model_str.joblib       # Short-term model
│   └── model_ltr.joblib       # Long-term model
│
├── notebooks/
│   ├── model - long-term.ipynb   # Long-term model training
│   └── model - short-term.ipynb  # Short-term model training
│
├── templates/                  # HTML templates
│   ├── index.html
│   ├── corrosion_calculator.html
│   ├── fluid_sampling.html
│   ├── short_term.html
│   └── long_term.html
│
├── static/                     # Static files
│   └── style.css
│
└── docs/                       # Documentation
    ├── DEPLOYMENT_GUIDE.md
    ├── PRODUCTION_READY.md
    └── API_DOCS.md
```

---

## 🔌 API Endpoints

### Health Check
```http
GET /health
```

**Response:**
```json
{
  "status": "healthy",
  "version": "2.0.1",
  "models": {
    "fluid_sampling": true,
    "short_term": true,
    "long_term": true
  }
}
```

---

### Fluid Sampling Prediction
```http
POST /api/predict-fluid-sampling
Content-Type: application/json
```

**Request:**
```json
{
  "equipment": "Storage Tank",
  "part": "Shell",
  "ou": "HO",
  "cation_anion_balance": 0,
  "hco3": 120,
  "density": 1.02,
  "resistivity": 3000,
  "ph": 7.1,
  "salinity": 15000,
  "so4": 50,
  "ca": 120,
  "mg": 80,
  "acetic_acid": 5
}
```

**Response:**
```json
{
  "success": true,
  "predicted_corrosion_rate": 0.123,
  "equipment_info": {
    "equipment": "Storage Tank",
    "part": "Shell",
    "ou": "HO"
  }
}
```

---

### Short Term Prediction
```http
POST /api/predict-short-term
Content-Type: application/json
```

**Request:**
```json
{
  "equipment": "Storage Tank",
  "part": "Shell",
  "ou": "HO"
}
```

---

### Long Term Prediction
```http
POST /api/predict-long-term
Content-Type: application/json
```

**Request:**
```json
{
  "equipment": "Storage Tank",
  "part": "Shell",
  "ou": "HO"
}
```

---

## 🐳 Docker Deployment

### Build Docker Image
```bash
docker build -t corrosion-rate-app .
```

### Run Container
```bash
docker run -p 5000:5000 corrosion-rate-app
```

### Docker Compose
```bash
docker-compose up -d
```

---

## 🌐 Production Deployment

### Option 1: Waitress (Windows)
```bash
pip install waitress
waitress-serve --host=0.0.0.0 --port=5000 --threads=4 wsgi:app
```

### Option 2: Gunicorn (Linux)
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 --timeout 120 wsgi:app
```

### Option 3: Nginx Reverse Proxy
See `docs/DEPLOYMENT_GUIDE.md` for detailed configuration.

---

## ⚙️ Configuration

Create `.env` file:
```bash
FLASK_HOST=0.0.0.0
FLASK_PORT=5000
FLASK_DEBUG=False
```

---

## 🧪 Testing

### Health Check
```bash
curl http://localhost:5000/health
```

### Test Prediction
```bash
curl -X POST http://localhost:5000/api/predict-fluid-sampling \
  -H "Content-Type: application/json" \
  -d @test_data.json
```

---

## 📊 Tech Stack

- **Backend:** Flask 3.1.0
- **ML Libraries:** 
  - Scikit-learn 1.9.0
  - Pandas 3.0.3
  - NumPy 2.4.6
  - Category Encoders 2.8.1
- **Frontend:** HTML5, CSS3, JavaScript
- **Visualization:** Chart.js
- **Production Server:** Waitress / Gunicorn

---

## 📚 Documentation

- [Deployment Guide](docs/DEPLOYMENT_GUIDE.md) - Complete deployment instructions
- [Production Ready](docs/PRODUCTION_READY.md) - Production checklist and features
- [API Documentation](docs/API_DOCS.md) - Complete API reference
- [Update Notes](docs/UPDATE_NOTES.md) - Version history and bug fixes

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 👥 Authors

- **Your Name** - *Initial work*

---

## 🙏 Acknowledgments

- Scikit-learn team for excellent ML library
- Flask team for robust web framework
- Contributors and testers

---

## 📞 Support

For issues, questions, or suggestions:
- Open an issue on GitHub
- Email: your.email@example.com

---

## 🔄 Version History

### v2.0.1 (Current)
- ✅ Fixed fluid sampling validation bug
- ✅ Added equipment info to fluid sampling
- ✅ Production ready features
- ✅ Complete documentation

### v2.0.0
- ✨ Redesigned fluid sampling with ML prediction
- ✨ Added 3 equipment info fields
- ✨ Health check endpoint
- ✨ Production WSGI support

### v1.0.0
- 🎉 Initial release
- ✨ 4 menu features
- ✨ 3 ML models
- ✨ Basic web interface

---

**Made with ❤️ for corrosion prediction**
