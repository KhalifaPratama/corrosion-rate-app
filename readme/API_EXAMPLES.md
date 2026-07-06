# 🔌 API Examples - Corrosion Rate Application

Dokumentasi lengkap dan contoh penggunaan API endpoints.

---

## 📋 Base URL

```
http://localhost:5000
```

---

## 1️⃣ Calculate Corrosion Rate

### Endpoint
```
POST /api/calculate-corrosion
```

### Description
Menghitung laju korosi berdasarkan parameter equipment (bottom, shell, atau roof).

### Headers
```json
Content-Type: application/json
```

### Request Body Examples

#### Example 1: Bottom Calculation
```json
{
  "part": "bottom",
  "actual_thickness": 10.0,
  "min_thickness": 2.5,
  "year": 2024,
  "soil_resistivity": 5000,
  "srb_count": 1000
}
```

#### Example 2: Shell Calculation
```json
{
  "part": "shell",
  "actual_thickness": 12.0,
  "min_thickness": 3.0,
  "year": 2024,
  "temperature": 40.0,
  "water_content": 0.5
}
```

#### Example 3: Roof Calculation
```json
{
  "part": "roof",
  "actual_thickness": 8.0,
  "min_thickness": 2.0,
  "year": 2024,
  "h2s": 10.0,
  "humidity": 80.0
}
```

### Success Response
```json
{
  "success": true,
  "corrosion_rate": 1.200,
  "remaining_life": 6.3,
  "retirement_year": 2030
}
```

### Error Response
```json
{
  "success": false,
  "error": "Missing required parameter: soil_resistivity"
}
```

### cURL Example
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

### JavaScript Fetch Example
```javascript
async function calculateCorrosion() {
  const response = await fetch('http://localhost:5000/api/calculate-corrosion', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      part: 'bottom',
      actual_thickness: 10.0,
      min_thickness: 2.5,
      year: 2024,
      soil_resistivity: 5000,
      srb_count: 1000
    })
  });
  
  const result = await response.json();
  console.log(result);
}
```

### Python Requests Example
```python
import requests
import json

url = "http://localhost:5000/api/calculate-corrosion"
data = {
    "part": "bottom",
    "actual_thickness": 10.0,
    "min_thickness": 2.5,
    "year": 2024,
    "soil_resistivity": 5000,
    "srb_count": 1000
}

response = requests.post(url, json=data)
result = response.json()
print(result)
```

---

## 2️⃣ Predict Short Term

### Endpoint
```
POST /api/predict-short-term
```

### Description
Prediksi laju korosi jangka pendek (1-3 bulan) menggunakan machine learning model.

### Headers
```json
Content-Type: application/json
```

### Request Body
```json
{
  "pH": 7.0,
  "temperature": 25.0,
  "chloride": 100.0,
  "oxygen": 5.0,
  "flow_rate": 1.0
}
```

### Example with Different Values
```json
{
  "pH": 6.5,
  "temperature": 35.0,
  "chloride": 250.0,
  "oxygen": 8.0,
  "flow_rate": 2.5
}
```

### Success Response
```json
{
  "success": true,
  "predicted_corrosion_rate": 0.145
}
```

### Error Response (Model Not Loaded)
```json
{
  "success": false,
  "error": "Model Short-Term belum dimuat"
}
```

### cURL Example
```bash
curl -X POST http://localhost:5000/api/predict-short-term \
  -H "Content-Type: application/json" \
  -d '{
    "pH": 7.0,
    "temperature": 25.0,
    "chloride": 100.0,
    "oxygen": 5.0,
    "flow_rate": 1.0
  }'
```

### JavaScript Fetch Example
```javascript
async function predictShortTerm() {
  const response = await fetch('http://localhost:5000/api/predict-short-term', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      pH: 7.0,
      temperature: 25.0,
      chloride: 100.0,
      oxygen: 5.0,
      flow_rate: 1.0
    })
  });
  
  const result = await response.json();
  console.log(`Predicted CR: ${result.predicted_corrosion_rate} mm/year`);
}
```

### Python Requests Example
```python
import requests

url = "http://localhost:5000/api/predict-short-term"
data = {
    "pH": 7.0,
    "temperature": 25.0,
    "chloride": 100.0,
    "oxygen": 5.0,
    "flow_rate": 1.0
}

response = requests.post(url, json=data)
result = response.json()

if result['success']:
    print(f"Predicted Corrosion Rate: {result['predicted_corrosion_rate']} mm/year")
else:
    print(f"Error: {result['error']}")
```

---

## 3️⃣ Predict Long Term

### Endpoint
```
POST /api/predict-long-term
```

### Description
Prediksi laju korosi jangka panjang (1-10 tahun) untuk perencanaan maintenance.

### Headers
```json
Content-Type: application/json
```

### Request Body
```json
{
  "pH": 7.0,
  "temperature": 25.0,
  "chloride": 100.0,
  "sulfate": 50.0,
  "hardness": 200.0,
  "alkalinity": 100.0
}
```

### Example with Aggressive Environment
```json
{
  "pH": 5.5,
  "temperature": 40.0,
  "chloride": 500.0,
  "sulfate": 200.0,
  "hardness": 350.0,
  "alkalinity": 50.0
}
```

### Success Response
```json
{
  "success": true,
  "predicted_corrosion_rate": 0.125
}
```

### Error Response (Model Not Loaded)
```json
{
  "success": false,
  "error": "Model Long-Term belum dimuat"
}
```

### cURL Example
```bash
curl -X POST http://localhost:5000/api/predict-long-term \
  -H "Content-Type: application/json" \
  -d '{
    "pH": 7.0,
    "temperature": 25.0,
    "chloride": 100.0,
    "sulfate": 50.0,
    "hardness": 200.0,
    "alkalinity": 100.0
  }'
```

### JavaScript Fetch Example
```javascript
async function predictLongTerm() {
  const response = await fetch('http://localhost:5000/api/predict-long-term', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      pH: 7.0,
      temperature: 25.0,
      chloride: 100.0,
      sulfate: 50.0,
      hardness: 200.0,
      alkalinity: 100.0
    })
  });
  
  const result = await response.json();
  
  if (result.success) {
    const remainingLife = 10 / result.predicted_corrosion_rate; // Assuming 10mm thickness
    console.log(`Predicted CR: ${result.predicted_corrosion_rate} mm/year`);
    console.log(`Est. Remaining Life: ${remainingLife.toFixed(1)} years`);
  }
}
```

### Python Requests Example
```python
import requests

url = "http://localhost:5000/api/predict-long-term"
data = {
    "pH": 7.0,
    "temperature": 25.0,
    "chloride": 100.0,
    "sulfate": 50.0,
    "hardness": 200.0,
    "alkalinity": 100.0
}

response = requests.post(url, json=data)
result = response.json()

if result['success']:
    cr = result['predicted_corrosion_rate']
    remaining_life = 10 / cr  # Assuming 10mm thickness
    print(f"Predicted CR: {cr} mm/year")
    print(f"Estimated Remaining Life: {remaining_life:.1f} years")
```

---

## 4️⃣ Save Fluid Sample

### Endpoint
```
POST /api/save-fluid-sample
```

### Description
Menyimpan data sampling fluida untuk dokumentasi dan analisis.

### Headers
```json
Content-Type: application/json
```

### Request Body (Minimal)
```json
{
  "sample_id": "FS-2024-001",
  "sample_date": "2024-01-15",
  "location": "Tank-101"
}
```

### Request Body (Complete)
```json
{
  "sample_id": "FS-2024-001",
  "sample_date": "2024-01-15",
  "location": "Tank-101",
  "equipment_type": "tank",
  "pH": 7.0,
  "temperature": 25.0,
  "chloride": 100.0,
  "sulfate": 50.0,
  "oxygen": 5.0,
  "co2": 0.5,
  "h2s": 2.0,
  "hardness": 200.0,
  "alkalinity": 100.0,
  "conductivity": 500.0,
  "iron": 0.5,
  "water_content": 0.1,
  "flow_rate": 1.0,
  "pressure": 5.0,
  "srb_count": 1000,
  "notes": "Routine sampling - normal conditions"
}
```

### Success Response
```json
{
  "success": true,
  "message": "Data sampling berhasil disimpan",
  "sample_id": "FS-2024-001"
}
```

### Error Response (Missing Field)
```json
{
  "success": false,
  "error": "Field sample_id diperlukan"
}
```

### cURL Example
```bash
curl -X POST http://localhost:5000/api/save-fluid-sample \
  -H "Content-Type: application/json" \
  -d '{
    "sample_id": "FS-2024-001",
    "sample_date": "2024-01-15",
    "location": "Tank-101",
    "pH": 7.0,
    "temperature": 25.0,
    "chloride": 100.0
  }'
```

### JavaScript Fetch Example
```javascript
async function saveFluidSample() {
  const sampleData = {
    sample_id: "FS-2024-001",
    sample_date: "2024-01-15",
    location: "Tank-101",
    pH: 7.0,
    temperature: 25.0,
    chloride: 100.0,
    notes: "Routine sampling"
  };
  
  const response = await fetch('http://localhost:5000/api/save-fluid-sample', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(sampleData)
  });
  
  const result = await response.json();
  console.log(result.message);
}
```

### Python Requests Example
```python
import requests
from datetime import date

url = "http://localhost:5000/api/save-fluid-sample"
data = {
    "sample_id": "FS-2024-001",
    "sample_date": str(date.today()),
    "location": "Tank-101",
    "pH": 7.0,
    "temperature": 25.0,
    "chloride": 100.0,
    "sulfate": 50.0,
    "oxygen": 5.0,
    "notes": "Routine sampling"
}

response = requests.post(url, json=data)
result = response.json()

if result['success']:
    print(f"Sample {result['sample_id']} saved successfully!")
else:
    print(f"Error: {result['error']}")
```

---

## 🧪 Testing with Postman

### 1. Import Collection

Create a new Postman collection with these endpoints:

```json
{
  "info": {
    "name": "Corrosion Rate API",
    "schema": "https://schema.getpostman.com/json/collection/v2.1.0/collection.json"
  },
  "item": [
    {
      "name": "Calculate Corrosion",
      "request": {
        "method": "POST",
        "header": [{"key": "Content-Type", "value": "application/json"}],
        "body": {
          "mode": "raw",
          "raw": "{\n  \"part\": \"bottom\",\n  \"actual_thickness\": 10.0,\n  \"min_thickness\": 2.5,\n  \"year\": 2024,\n  \"soil_resistivity\": 5000,\n  \"srb_count\": 1000\n}"
        },
        "url": {"raw": "http://localhost:5000/api/calculate-corrosion"}
      }
    }
  ]
}
```

---

## 📊 Response Status Codes

| Code | Meaning | Description |
|------|---------|-------------|
| 200 | OK | Request successful |
| 400 | Bad Request | Invalid input or missing parameters |
| 500 | Internal Server Error | Model not loaded or server error |

---

## 🔍 Error Handling Examples

### Handle Network Errors (JavaScript)
```javascript
async function callAPI(endpoint, data) {
  try {
    const response = await fetch(endpoint, {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify(data)
    });
    
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    
    const result = await response.json();
    
    if (!result.success) {
      throw new Error(result.error);
    }
    
    return result;
  } catch (error) {
    console.error('API Error:', error.message);
    throw error;
  }
}
```

### Handle Errors (Python)
```python
import requests

def call_api(endpoint, data):
    try:
        response = requests.post(endpoint, json=data, timeout=10)
        response.raise_for_status()
        
        result = response.json()
        
        if not result.get('success', False):
            raise ValueError(result.get('error', 'Unknown error'))
        
        return result
    
    except requests.exceptions.Timeout:
        print("Request timed out")
    except requests.exceptions.ConnectionError:
        print("Connection error")
    except requests.exceptions.HTTPError as e:
        print(f"HTTP error: {e}")
    except ValueError as e:
        print(f"API error: {e}")
```

---

## 🚀 Integration Examples

### React Component Example
```jsx
import React, { useState } from 'react';

function CorrosionCalculator() {
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const calculateCorrosion = async (data) => {
    setLoading(true);
    try {
      const response = await fetch('http://localhost:5000/api/calculate-corrosion', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify(data)
      });
      const result = await response.json();
      setResult(result);
    } catch (error) {
      console.error('Error:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      {loading && <p>Calculating...</p>}
      {result && (
        <div>
          <p>Corrosion Rate: {result.corrosion_rate} mm/year</p>
          <p>Remaining Life: {result.remaining_life} years</p>
        </div>
      )}
    </div>
  );
}
```

### Vue.js Example
```vue
<template>
  <div>
    <button @click="predict">Predict</button>
    <div v-if="result">
      <p>CR: {{ result.predicted_corrosion_rate }} mm/year</p>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      result: null
    }
  },
  methods: {
    async predict() {
      const response = await fetch('http://localhost:5000/api/predict-short-term', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({
          pH: 7.0,
          temperature: 25.0,
          chloride: 100.0,
          oxygen: 5.0,
          flow_rate: 1.0
        })
      });
      this.result = await response.json();
    }
  }
}
</script>
```

---

## 📝 Notes

1. **CORS**: Jika menggunakan dari domain berbeda, aktifkan CORS di Flask:
   ```python
   from flask_cors import CORS
   app = Flask(__name__)
   CORS(app)
   ```

2. **Authentication**: Untuk production, tambahkan authentication:
   ```python
   from flask_httpauth import HTTPBasicAuth
   ```

3. **Rate Limiting**: Implementasi rate limiting untuk mencegah abuse:
   ```python
   from flask_limiter import Limiter
   ```

4. **Validation**: Semua input sudah divalidasi di backend, tapi frontend validation direkomendasikan untuk UX yang lebih baik.

---

**Happy Coding! 🚀**
