from flask import Flask, request, jsonify, render_template
import numpy as np
import os
import sys

# PyInstaller compatibility: Get the correct base path
if getattr(sys, 'frozen', False):
    # Running as compiled executable
    base_path = sys._MEIPASS
else:
    # Running as normal Python script
    base_path = os.path.dirname(os.path.abspath(__file__))

# Try to import joblib (optional for ML models)
try:
    import joblib
    JOBLIB_AVAILABLE = True
except ImportError:
    JOBLIB_AVAILABLE = False
    print("⚠️ Warning: joblib not installed. ML predictions will not be available.")

# Try to import pickle for fluid sampling model
try:
    import pickle
    PICKLE_AVAILABLE = True
except ImportError:
    PICKLE_AVAILABLE = False
    print("⚠️ Warning: pickle not available.")

app = Flask(__name__, 
            template_folder=os.path.join(base_path, 'templates'),
            static_folder=os.path.join(base_path, 'static'))

# Configuration
app.config['JSON_SORT_KEYS'] = False
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max request size

# Load models (only if joblib is available)
MODEL_STR = os.path.join(base_path, 'model_str.joblib')
MODEL_LTR = os.path.join(base_path, 'model_ltr.joblib')
MODEL_FLUID = os.path.join(base_path, 'corrosion-rate.pkl')

model_str = None
model_ltr = None
model_fluid = None

if JOBLIB_AVAILABLE:
    # Try to load Short-Term model with error handling
    try:
        if os.path.exists(MODEL_STR):
            model_str = joblib.load(MODEL_STR)
            print(f"✅ Model Short-Term '{MODEL_STR}' berhasil dimuat.")
    except NotImplementedError as e:
        print(f"⚠️ Info: Model Short-Term tidak kompatibel (pandas StringDtype issue).")
        print(f"   Solusi: Re-train model dari notebook 'model - short-term.ipynb'")
        print(f"   Atau jalankan: python retrain_shortterm.py")
        model_str = None
    except Exception as e:
        print(f"⚠️ Info: Model Short-Term tidak kompatibel dengan versi library saat ini.")
        print(f"   Detail: {type(e).__name__}")
        model_str = None

    # Try to load Long-Term model with error handling
    try:
        if os.path.exists(MODEL_LTR):
            model_ltr = joblib.load(MODEL_LTR)
            print(f"✅ Model Long-Term '{MODEL_LTR}' berhasil dimuat.")
    except NotImplementedError as e:
        print(f"⚠️ Info: Model Long-Term tidak kompatibel (pandas StringDtype issue).")
        print(f"   Solusi: Re-train model dari notebook 'model - long-term.ipynb'")
        model_ltr = None
    except Exception as e:
        print(f"⚠️ Info: Model Long-Term tidak kompatibel dengan versi library saat ini.")
        print(f"   Detail: {type(e).__name__}")
        model_ltr = None
else:
    print("ℹ️ Info: Aplikasi akan berjalan tanpa fitur ML prediction.")
    print("ℹ️ Info: Corrosion Calculator dan Fluid Sampling tetap berfungsi.")

# Load Fluid Sampling model (pickle format)
if PICKLE_AVAILABLE:
    try:
        if os.path.exists(MODEL_FLUID):
            with open(MODEL_FLUID, 'rb') as file:
                model_fluid = pickle.load(file)
            print(f"✅ Model Fluid Sampling '{MODEL_FLUID}' berhasil dimuat.")
    except Exception as e:
        print(f"⚠️ Info: Model Fluid Sampling tidak kompatibel dengan versi library saat ini.")
        print(f"   Detail: {type(e).__name__}")
        model_fluid = None
else:
    print("ℹ️ Info: Fluid Sampling model tidak dapat dimuat (pickle not available).")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/health')
def health_check():
    """Health check endpoint for monitoring"""
    return jsonify({
        'status': 'healthy',
        'version': '2.0',
        'models': {
            'fluid_sampling': model_fluid is not None,
            'short_term': model_str is not None,
            'long_term': model_ltr is not None
        }
    })

@app.route('/corrosion-calculator')
def corrosion_calculator():
    return render_template('corrosion_calculator.html')

@app.route('/fluid-sampling')
def fluid_sampling():
    return render_template('fluid_sampling.html')

@app.route('/short-term')
def short_term():
    return render_template('short_term.html')

@app.route('/long-term')
def long_term():
    return render_template('long_term.html')

# API Endpoints
@app.route('/api/calculate-corrosion', methods=['POST'])
def calculate_corrosion():
    """Calculate corrosion rate based on equipment parameters"""
    try:
        data = request.get_json()
        
        part_value = data.get('part', 'bottom')
        t_act = float(data.get('actual_thickness', 10.0))
        t_min = float(data.get('min_thickness', 2.5))
        start_year = int(data.get('year', 2024))
        
        cr = 0.1  # Default corrosion rate
        
        if part_value == 'bottom':
            res = float(data.get('soil_resistivity', 5000))
            srb = float(data.get('srb_count', 1000))
            cr = (srb / 1000) + (1000 / res)
        elif part_value == 'shell':
            temp = float(data.get('temperature', 40))
            water = float(data.get('water_content', 0.5))
            cr = (temp * 0.005) + (water * 0.1)
        elif part_value == 'roof':
            h2s = float(data.get('h2s', 10))
            hum = float(data.get('humidity', 80))
            cr = (h2s * 0.01) + (hum / 400)
        
        rl = (t_act - t_min) / cr if cr > 0 else 0
        retirement_year = int(start_year + max(0, rl))
        
        return jsonify({
            'success': True,
            'corrosion_rate': round(cr, 3),
            'remaining_life': round(max(0, rl), 1),
            'retirement_year': retirement_year
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400

@app.route('/api/predict-short-term', methods=['POST'])
def predict_short_term():
    """Predict short-term corrosion rate using ML model"""
    if model_str is None:
        return jsonify({
            'success': False, 
            'error': 'Model Short-Term belum dimuat atau tidak kompatibel'
        }), 500
    
    try:
        data = request.get_json()
        
        # Extract features sesuai model notebook
        # Model menggunakan: equipment, part, ou
        equipment = data.get('equipment', 'Storage Tank')
        part = data.get('part', 'Shell')
        ou = data.get('ou', 'HO')  # Operating Unit
        
        # Create DataFrame with exact column names as in training
        import pandas as pd
        input_data = pd.DataFrame({
            'equipment': [equipment],
            'part': [part],
            'ou': [ou]
        })
        
        # Predict using the pipeline (TargetEncoder + RandomForest)
        prediction = model_str.predict(input_data)
        
        return jsonify({
            'success': True,
            'predicted_corrosion_rate': round(float(prediction[0]), 3),
            'input': {
                'equipment': equipment,
                'part': part,
                'ou': ou
            }
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400

@app.route('/api/predict-long-term', methods=['POST'])
def predict_long_term():
    """Predict long-term corrosion rate using ML model"""
    if model_ltr is None:
        return jsonify({
            'success': False, 
            'error': 'Model Long-Term belum dimuat atau tidak kompatibel'
        }), 500
    
    try:
        data = request.get_json()
        
        # Extract features sesuai model notebook
        # Model menggunakan: equipment, part, ou
        equipment = data.get('equipment', 'Storage Tank')
        part = data.get('part', 'Shell')
        ou = data.get('ou', 'HO')  # Operating Unit
        
        # Create DataFrame with exact column names as in training
        import pandas as pd
        input_data = pd.DataFrame({
            'equipment': [equipment],
            'part': [part],
            'ou': [ou]
        })
        
        # Predict using the pipeline (TargetEncoder + RandomForest)
        prediction = model_ltr.predict(input_data)
        
        return jsonify({
            'success': True,
            'predicted_corrosion_rate': round(float(prediction[0]), 3),
            'input': {
                'equipment': equipment,
                'part': part,
                'ou': ou
            }
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400

@app.route('/api/save-fluid-sample', methods=['POST'])
def save_fluid_sample():
    """Save fluid sampling data"""
    try:
        data = request.get_json()
        
        # In production, save to database
        # For now, just validate and return success
        required_fields = ['sample_id', 'sample_date', 'location']
        for field in required_fields:
            if field not in data:
                return jsonify({'success': False, 'error': f'Field {field} diperlukan'}), 400
        
        return jsonify({
            'success': True,
            'message': 'Data sampling berhasil disimpan',
            'sample_id': data['sample_id']
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400

@app.route('/api/predict-fluid-sampling', methods=['POST'])
def predict_fluid_sampling():
    """Predict corrosion rate from fluid sampling parameters using corrosion-rate.pkl model"""
    if model_fluid is None:
        return jsonify({
            'success': False, 
            'error': 'Model Fluid Sampling belum dimuat atau tidak kompatibel'
        }), 500
    
    try:
        data = request.get_json()
        
        # Extract equipment info (for display/logging only, not used in model)
        equipment = data.get('equipment', 'Unknown')
        part = data.get('part', 'Unknown')
        ou = data.get('ou', 'Unknown')
        
        # Extract 10 fluid parameters (sesuai model corrosion-rate.pkl)
        cation_anion_balance = float(data.get('cation_anion_balance', 0))
        hco3 = float(data.get('hco3', 120))
        density = float(data.get('density', 1.02))
        resistivity = float(data.get('resistivity', 3000))
        ph = float(data.get('ph', 7.1))
        salinity = float(data.get('salinity', 15000))
        so4 = float(data.get('so4', 50))
        ca = float(data.get('ca', 120))
        mg = float(data.get('mg', 80))
        acetic_acid = float(data.get('acetic_acid', 5))
        
        # Create feature array in correct order
        features = np.array([[
            cation_anion_balance, 
            hco3, 
            density, 
            resistivity, 
            ph, 
            salinity, 
            so4, 
            ca, 
            mg, 
            acetic_acid
        ]])
        
        # Predict using the model
        prediction = model_fluid.predict(features)
        
        return jsonify({
            'success': True,
            'predicted_corrosion_rate': round(float(prediction[0]), 3),
            'equipment_info': {
                'equipment': equipment,
                'part': part,
                'ou': ou
            },
            'input': {
                'cation_anion_balance': cation_anion_balance,
                'hco3': hco3,
                'density': density,
                'resistivity': resistivity,
                'ph': ph,
                'salinity': salinity,
                'so4': so4,
                'ca': ca,
                'mg': mg,
                'acetic_acid': acetic_acid
            }
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400

# Error Handlers
@app.errorhandler(404)
def not_found_error(error):
    return jsonify({'error': 'Resource not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal server error'}), 500

@app.errorhandler(413)
def request_entity_too_large(error):
    return jsonify({'error': 'Request too large'}), 413

if __name__ == '__main__':
    import os
    
    # Get configuration from environment variables
    host = os.getenv('FLASK_HOST', '0.0.0.0')
    port = int(os.getenv('FLASK_PORT', 5000))
    debug = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'
    
    print(f"\n{'='*50}")
    print(f"Starting Corrosion Rate Application")
    print(f"Host: {host}")
    print(f"Port: {port}")
    print(f"Debug Mode: {debug}")
    print(f"{'='*50}\n")
    
    app.run(debug=debug, host=host, port=port)
