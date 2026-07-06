# 🔧 Manual Installation Guide

Jika `install.bat` mengalami error, ikuti langkah manual berikut:

---

## ⚠️ Troubleshooting Install.bat Errors

### Error 1: "Python is not recognized"

**Penyebab:** Python tidak terinstall atau tidak ada di PATH

**Solusi:**
1. Download Python dari https://www.python.org/downloads/
2. Install Python, **PASTIKAN centang "Add Python to PATH"**
3. Restart Command Prompt
4. Test: `python --version`

---

### Error 2: "pip is not recognized"

**Penyebab:** pip tidak terinstall atau tidak ada di PATH

**Solusi:**
```bash
# Download get-pip.py
curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py

# Install pip
python get-pip.py
```

---

### Error 3: "Permission Denied" atau "Access Denied"

**Penyebab:** Tidak ada permission untuk install

**Solusi 1:** Run as Administrator
- Klik kanan `install.bat`
- Pilih "Run as administrator"

**Solusi 2:** Install untuk user saja
```bash
pip install --user -r requirements.txt
```

---

### Error 4: Specific package installation failed

**Solusi:** Install package secara manual satu per satu

```bash
python -m pip install Flask==3.0.0
python -m pip install numpy==1.24.3
python -m pip install pandas==2.0.3
python -m pip install scikit-learn==1.3.0
python -m pip install joblib==1.3.2
python -m pip install matplotlib==3.7.2
python -m pip install seaborn==0.12.2
```

---

## 📝 Manual Installation Steps

### Method 1: Using requirements.txt

```bash
# 1. Open Command Prompt
# Press Win + R, type cmd, press Enter

# 2. Navigate to project folder
cd d:\Documents\Alif\magangG8\nano\kalkulator-CR

# 3. Upgrade pip
python -m pip install --upgrade pip

# 4. Install dependencies
pip install -r requirements.txt
```

### Method 2: Using python -m pip

```bash
# 1. Open Command Prompt

# 2. Navigate to project folder
cd d:\Documents\Alif\magangG8\nano\kalkulator-CR

# 3. Install using python module
python -m pip install -r requirements.txt
```

### Method 3: Install packages individually

```bash
# 1. Open Command Prompt

# 2. Install each package
python -m pip install Flask
python -m pip install numpy
python -m pip install pandas
python -m pip install scikit-learn
python -m pip install joblib
python -m pip install matplotlib
python -m pip install seaborn
```

### Method 4: Using alternative installer

```bash
# Run the alternative installer
install-alternative.bat
```

---

## ✅ Verify Installation

After installation, verify that packages are installed:

```bash
# Check installed packages
pip list

# Or check specific packages
pip show Flask
pip show numpy
pip show pandas
pip show scikit-learn
```

Expected output should show all packages installed.

---

## 🚀 Run the Application

Once installation is successful:

```bash
# Method 1: Using batch file
run.bat

# Method 2: Direct command
python app.py

# Method 3: Using python -m
python -m flask run
```

Then open browser at: **http://localhost:5000**

---

## 🔍 Common Issues & Solutions

### Issue: "Module not found" when running app

**Solution:**
```bash
# Reinstall the missing module
pip install <module-name>

# Example:
pip install Flask
```

### Issue: Port 5000 already in use

**Solution:**
Edit `app.py`, change the last line:
```python
app.run(debug=True, host='0.0.0.0', port=5001)
```

### Issue: "ImportError: DLL load failed"

**Penyebab:** Missing Visual C++ Redistributable (for numpy, pandas)

**Solution:**
1. Download Microsoft Visual C++ Redistributable:
   https://aka.ms/vs/17/release/vc_redist.x64.exe
2. Install it
3. Reinstall Python packages

### Issue: Installation is too slow

**Solution:** Use a mirror
```bash
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
```

---

## 🐍 Python Version Compatibility

**Recommended:** Python 3.8 - 3.11

**Check your version:**
```bash
python --version
```

If version is < 3.7 or > 3.11:
- Download compatible version from https://www.python.org/
- Install alongside current version (don't uninstall old one)
- Use specific version: `py -3.10 -m pip install -r requirements.txt`

---

## 💡 Alternative: Use Virtual Environment

For cleaner installation:

```bash
# 1. Create virtual environment
python -m venv venv

# 2. Activate it
# For Windows Command Prompt:
venv\Scripts\activate.bat

# For Windows PowerShell:
venv\Scripts\Activate.ps1

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run app
python app.py
```

To deactivate virtual environment:
```bash
deactivate
```

---

## 🆘 Still Having Issues?

### Option 1: Use lightweight versions

Create `requirements-light.txt`:
```
Flask
numpy
pandas
scikit-learn
joblib
```

Then install:
```bash
pip install -r requirements-light.txt
```

### Option 2: Skip ML packages

For basic functionality (Corrosion Calculator & Fluid Sampling only):
```bash
pip install Flask numpy
```

App will work without ML models!

### Option 3: Use Conda (if available)

```bash
conda create -n corrosion python=3.10
conda activate corrosion
conda install flask numpy pandas scikit-learn
pip install joblib
```

---

## 📊 Installation Checklist

Before running the app, ensure:

- [x] Python 3.7+ installed
- [x] pip installed and working
- [x] All packages from requirements.txt installed
- [x] No error messages during installation
- [x] `pip list` shows all required packages

Optional:
- [ ] model_str.joblib exists (for Short Term)
- [ ] model_ltr.joblib exists (for Long Term)

---

## 🎯 Quick Test

After installation, test if it works:

```bash
# Test 1: Check Flask
python -c "import flask; print('Flask OK')"

# Test 2: Check numpy
python -c "import numpy; print('Numpy OK')"

# Test 3: Check pandas
python -c "import pandas; print('Pandas OK')"

# Test 4: Check scikit-learn
python -c "import sklearn; print('Sklearn OK')"

# Test 5: Run app
python app.py
```

If all tests pass, open browser at http://localhost:5000

---

## 📞 Additional Help

If you still encounter issues:

1. Check Python PATH: `echo %PATH%`
2. Check pip location: `where pip`
3. Check Python location: `where python`
4. Try PowerShell instead of CMD
5. Try running as Administrator
6. Restart computer after Python installation

---

**Good luck! 🚀**
