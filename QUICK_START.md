# 🚀 Quick Start Guide

## For Developers (Clone & Run)

```bash
# 1. Clone repository
git clone https://github.com/YOUR_USERNAME/corrosion-rate-app.git
cd corrosion-rate-app

# 2. Create virtual environment
python -m venv venv

# 3. Activate virtual environment
# Windows:
.\venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# 4. Install dependencies
pip install -r requirements.txt

# 5. Run application
python app.py

# 6. Open browser
http://localhost:5000
```

---

## For Production Deployment

```bash
# Windows (Waitress)
pip install waitress
waitress-serve --host=0.0.0.0 --port=5000 --threads=4 wsgi:app

# Linux (Gunicorn)
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 --timeout 120 wsgi:app
```

---

## Testing

```bash
# Health check
curl http://localhost:5000/health

# Should return:
{"status": "healthy", "models": {...}}
```

---

**For detailed instructions, see:**
- [README.md](README.md) - Full documentation
- [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md) - Production deployment
- [GIT_SETUP.md](GIT_SETUP.md) - Git repository setup
- [CHANGELOG.md](CHANGELOG.md) - Version history
