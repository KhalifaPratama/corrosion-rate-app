from flask import Flask, request, jsonify, render_template
import numpy as np
import pandas as pd  # Import at module level for better performance
import json
import os
import sys

# Konsol Windows default memakai code page 437/1252 yang tidak bisa menampilkan
# emoji pada pesan startup di bawah. Tanpa ini print() melempar
# UnicodeEncodeError dan aplikasi mati sebelum server jalan — di jendela .bat
# errornya cuma berkelip lalu hilang. errors='replace' cukup: karakter yang
# tidak didukung diganti '?', teksnya tetap terbaca.
for _stream in (sys.stdout, sys.stderr):
    try:
        _stream.reconfigure(errors='replace')
    except (AttributeError, ValueError):
        pass

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
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 31536000  # Cache static files for 1 year

# Enable response compression if available
try:
    from flask_compress import Compress
    Compress(app)
    print("✅ Response compression enabled (gzip)")
except ImportError:
    print("ℹ️ flask-compress not installed. Install with: pip install flask-compress")

# Load models (only if joblib is available)
# Short-Term  : 'model - stcr.joblib'  -> XGBRegressor, target str_p90
# Long-Term   : 'model - ltcr.joblib'  -> RandomForestRegressor, target ltr_p50
# Keduanya adalah Pipeline(OneHotEncoder(handle_unknown='ignore') -> regressor)
# dengan 6 fitur kategorikal yang sama (lihat MODEL_FEATURES).
MODEL_STCR = os.path.join(base_path, 'model - stcr.joblib')
MODEL_LTCR = os.path.join(base_path, 'model - ltcr.joblib')
MODEL_FLUID = os.path.join(base_path, 'corrosion-rate.pkl')

# Urutan kolom wajib sama persis dengan saat training (pipeline.feature_names_in_)
MODEL_FEATURES = ['equipment_type', 'category', 'part', 'asset_owner', 'ou', 'facility']

# Cakupan training kedua model tidak sama, dan OneHotEncoder di-training dengan
# handle_unknown='ignore': nilai di luar vocabulary tidak error, melainkan
# di-encode nol. Model tetap mengeluarkan angka, tapi kontribusi nilai tersebut
# hilang tanpa jejak — mis. input FFC dan string ngawur menghasilkan prediksi
# yang identik pada model short-term.
#
# Karena itu prediksi hanya dilaporkan bila SELURUH fitur dikenal model yang
# bersangkutan; bila ada satu saja yang asing, hasilnya N/A (lihat
# _run_prediction). Konsekuensinya cukup besar untuk short-term — 344 dari 898
# kombinasi peralatan di data master jadi N/A (38%), terbanyak karena facility
# di luar 91 facility yang pernah dilatih — sedangkan long-term hanya 1
# kombinasi. Nilai yang memicunya ditandai ⚠ di dropdown sebelum menghitung.

model_stcr = None
model_ltcr = None
model_fluid = None


def _load_model(path, label, hint):
    """Load a joblib pipeline, returning None (with a readable message) on failure."""
    if not os.path.exists(path):
        print(f"⚠️ Info: File model {label} tidak ditemukan: {path}")
        return None
    try:
        model = joblib.load(path)
        print(f"✅ Model {label} '{os.path.basename(path)}' berhasil dimuat.")
        return model
    except ModuleNotFoundError as e:
        print(f"⚠️ Info: Model {label} butuh library yang belum terinstall: {e.name}")
        print(f"   Solusi: pip install {e.name}")
        return None
    except Exception as e:
        print(f"⚠️ Info: Model {label} tidak kompatibel dengan versi library saat ini.")
        print(f"   Detail: {type(e).__name__} - {e}")
        print(f"   Solusi: re-train dari notebook '{hint}'")
        return None


def get_model_categories(pipeline):
    """
    Ambil daftar kategori yang dikenal model, per fitur, langsung dari
    OneHotEncoder hasil training. Dipakai untuk mengisi dropdown supaya
    pilihan di UI selalu sinkron dengan model (bukan hardcode).
    """
    if pipeline is None:
        return {}
    try:
        preprocessor = pipeline.named_steps['preprocessor']
        for _name, transformer, columns in preprocessor.transformers_:
            if hasattr(transformer, 'categories_'):
                return {
                    col: [str(v) for v in values]
                    for col, values in zip(columns, transformer.categories_)
                }
    except Exception as e:
        print(f"⚠️ Info: Gagal membaca kategori model: {type(e).__name__} - {e}")
    return {}


if JOBLIB_AVAILABLE:
    model_stcr = _load_model(MODEL_STCR, 'Short-Term (STCR p90)',
                             'model - stcr - p90_xgboost.ipynb')
    model_ltcr = _load_model(MODEL_LTCR, 'Long-Term (LTCR p50)',
                             'model - ltcr - p50_random forest.ipynb')
else:
    print("ℹ️ Info: Aplikasi akan berjalan tanpa fitur ML prediction.")
    print("ℹ️ Info: Corrosion Calculator dan Fluid Sampling tetap berfungsi.")

# Kategori per model + gabungan untuk dropdown.
STCR_CATEGORIES = get_model_categories(model_stcr)
LTCR_CATEGORIES = get_model_categories(model_ltcr)

MODEL_OPTIONS = {
    feature: sorted(
        set(STCR_CATEGORIES.get(feature, [])) | set(LTCR_CATEGORIES.get(feature, []))
    )
    for feature in MODEL_FEATURES
}

# Vocabulary model memuat seluruh bagian untuk semua jenis peralatan, padahal
# di lapangan beberapa jenis peralatan hanya punya satu bagian yang diinspeksi:
# FFC hanya plate (tube bundle), HEX hanya shell. Jenis peralatan yang tidak
# terdaftar di sini tetap menawarkan seluruh pilihan bagian.
PART_BY_EQUIPMENT = {
    'FFC': ['Plate'],
    'HEX': ['Shell'],
}

# --- Data master peralatan ---------------------------------------------------
# 'equipment_master.json' berisi kombinasi peralatan yang benar-benar ada di
# lapangan, dipakai agar dropdown saling menyaring: memilih OU menyisakan
# facility milik OU itu saja, bukan seluruh 186 facility tanpa konteks.
#
# File ini hasil turunan dari data master peralatan, sudah disaring saat dibuat:
#   - hanya 4 jenis peralatan yang relevan (Pressure Vessel, Storage Tank,
#     FFC, HEX);
#   - hanya kombinasi yang seluruh nilainya dikenal model, sehingga dropdown
#     tidak pernah menawarkan pilihan yang membuat prediksi meleset diam-diam.
#
# Formatnya terindeks (daftar nilai + baris berisi indeks) supaya payload ke
# browser kecil. Dibaca dengan modul json bawaan — tidak ada dependensi Excel.
MASTER_PATH = os.path.join(base_path, 'equipment_master.json')

MASTER_FIELDS = ['equipment_type', 'category', 'facility', 'asset_owner', 'ou']

# Kategori yang ikut terbawa ke data master tapi tidak berlaku untuk jenis
# peralatan tersebut, mis. HEX tidak punya gas boot. Disaring saat memuat supaya
# dropdown kategori hanya menawarkan kombinasi yang benar-benar mungkin.
MASTER_EXCLUDED_CATEGORIES = {
    'HEX': ['Boot / Gas Boot / Degassing'],
}


def filter_master_categories(data):
    """
    Buang baris dengan kombinasi jenis peralatan + kategori yang tidak berlaku.

    Kategorinya sendiri tidak dihapus dari daftar nilai — 'Boot / Gas Boot /
    Degassing' masih dipakai Pressure Vessel — hanya barisnya yang dibuang,
    dan dropdown di frontend dibangun dari baris, bukan dari daftar nilai.
    """
    i_type = data['fields'].index('equipment_type')
    i_cat = data['fields'].index('category')
    jenis = data['values']['equipment_type']
    kategori = data['values']['category']

    terlarang = {
        (jenis.index(t), kategori.index(c))
        for t, daftar in MASTER_EXCLUDED_CATEGORIES.items()
        if t in jenis
        for c in daftar
        if c in kategori
    }
    if not terlarang:
        return data

    sebelum = len(data['rows'])
    data['rows'] = [r for r in data['rows'] if (r[i_type], r[i_cat]) not in terlarang]
    dibuang = sebelum - len(data['rows'])
    if dibuang:
        print(f"ℹ️ Info: {dibuang} kombinasi peralatan disaring "
              f"(kategori tidak berlaku untuk jenis peralatannya).")
    return data


def load_equipment_master(path):
    """
    Muat tabel kombinasi peralatan.

    Mengembalikan None bila file tidak ada atau rusak, sehingga aplikasi tetap
    jalan dengan dropdown dari vocabulary model (tanpa penyaringan bertingkat).
    """
    if not os.path.exists(path):
        print(f"ℹ️ Info: '{os.path.basename(path)}' tidak ditemukan; "
              f"dropdown memakai vocabulary model tanpa penyaringan.")
        return None
    try:
        with open(path, encoding='utf-8') as f:
            data = json.load(f)

        if data.get('fields') != MASTER_FIELDS or not data.get('rows'):
            print("⚠️ Info: struktur data master tidak sesuai; diabaikan.")
            return None

        data = filter_master_categories(data)

        print(f"✅ Data master '{os.path.basename(path)}' dimuat: "
              f"{len(data['rows'])} kombinasi peralatan.")
        return data
    except Exception as e:
        print(f"⚠️ Info: gagal membaca data master: {type(e).__name__} - {e}")
        return None


EQUIPMENT_MASTER = load_equipment_master(MASTER_PATH)


def master_values_unknown_per_model():
    """
    Nilai yang ditawarkan dropdown tapi tidak dikenal masing-masing model.

    Cakupan training kedua model tidak sama — STCR jauh lebih sempit dan sama
    sekali tidak mengenal jenis peralatan FFC. Nilai seperti itu tetap
    ditawarkan (peralatannya memang ada di lapangan), tapi ditandai ⚠ di
    dropdown supaya pengguna tahu prediksi model tersebut tidak akan
    ditampilkan sebelum menekan Hitung, bukan baru setelah hasilnya keluar.

    Seluruh MODEL_FEATURES diperiksa, bukan hanya field data master: 'part'
    diambil dari vocabulary model karena tidak ada di master, dan nilai asing
    di sana ('Plate' pada model short-term) sama-sama membuat hasilnya N/A.
    """
    hasil = {}
    for label, katalog in (('short_term', STCR_CATEGORIES), ('long_term', LTCR_CATEGORIES)):
        per_field = {}
        for field in MODEL_FEATURES:
            dikenal = set(katalog.get(field, []))
            if not dikenal:
                continue
            if EQUIPMENT_MASTER and field in MASTER_FIELDS:
                ditawarkan = EQUIPMENT_MASTER['values'][field]
            else:
                ditawarkan = MODEL_OPTIONS.get(field, [])
            asing = [v for v in ditawarkan if v not in dikenal]
            if asing:
                per_field[field] = asing
        if per_field:
            hasil[label] = per_field
    return hasil

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

# --- Model Fluid Sampling khusus per Operating Unit ---------------------------
# 'model - fluid sampling - <OU>.joblib' adalah Pipeline(OneHotEncoder(Equipment)
# + passthrough parameter kimia -> RandomForestRegressor), target kolom 'CR'.
# Model ini hanya tersedia untuk OU tertentu; OU lain memakai model umum
# 'corrosion-rate.pkl' (SVR 10 fitur) yang tetap dipertahankan.
FLUID_OU_MODELS = {}

# Jumlah sampel latih per OU — dipakai untuk menyampaikan keterbatasan model ke pengguna.
FLUID_TRAIN_SAMPLES = {'SLN': 64, 'SLS': 37}

if JOBLIB_AVAILABLE:
    for _ou in ('SLN', 'SLS'):
        _path = os.path.join(base_path, f'model - fluid sampling - {_ou}.joblib')
        _model = _load_model(_path, f'Fluid Sampling {_ou}',
                             f'model - fluid sampling - {_ou}.ipynb')
        if _model is not None:
            FLUID_OU_MODELS[_ou] = _model

# Fitur model umum lama, memakai nama kolom asli saat training.
FLUID_LEGACY_FEATURES = [
    'Cation Anion Balance', 'HCO3', 'Density', 'Resistivity', 'pH',
    'Salinity', 'SO4', 'Ca', 'Mg', 'Acetic Acid'
]

# Alias key lama (snake_case) yang dipakai versi form sebelumnya.
FLUID_LEGACY_ALIASES = {
    'cation_anion_balance': 'Cation Anion Balance', 'hco3': 'HCO3',
    'density': 'Density', 'resistivity': 'Resistivity', 'ph': 'pH',
    'salinity': 'Salinity', 'so4': 'SO4', 'ca': 'Ca', 'mg': 'Mg',
    'acetic_acid': 'Acetic Acid',
}


def get_fluid_model_features(pipeline):
    """Daftar fitur numerik + opsi Equipment dari pipeline fluid sampling per-OU."""
    features = [str(f) for f in pipeline.feature_names_in_]
    equipment_options = []
    try:
        preprocessor = pipeline.named_steps['preprocessor']
        for _name, transformer, columns in preprocessor.transformers_:
            if hasattr(transformer, 'categories_') and 'Equipment' in list(columns):
                idx = list(columns).index('Equipment')
                equipment_options = [str(v) for v in transformer.categories_[idx]]
    except Exception as e:
        print(f"⚠️ Info: Gagal membaca opsi Equipment: {type(e).__name__} - {e}")
    numeric = [f for f in features if f != 'Equipment']
    return numeric, equipment_options


def predict_with_interval(pipeline, input_df):
    """
    Prediksi + rentang ketidakpastian dari sebaran pohon Random Forest.

    Tiap pohon memberi estimasi sendiri; persentil 10-90 dari sebaran itu
    dipakai sebagai rentang wajar. Model non-ensemble mengembalikan None.
    """
    prediction = float(pipeline.predict(input_df)[0])
    try:
        regressor = pipeline.steps[-1][1]
        estimators = getattr(regressor, 'estimators_', None)
        if not estimators:
            return prediction, None
        transformed = pipeline[:-1].transform(input_df)
        per_tree = np.array([float(t.predict(transformed)[0]) for t in estimators])
        low, high = np.percentile(per_tree, [10, 90])
        return prediction, {'low': round(float(low), 4), 'high': round(float(high), 4)}
    except Exception as e:
        print(f"⚠️ Info: Gagal menghitung rentang: {type(e).__name__} - {e}")
        return prediction, None


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
            'short_term': model_stcr is not None,
            'long_term': model_ltcr is not None
        }
    })

@app.route('/corrosion-calculator')
def corrosion_calculator():
    return render_template('corrosion_calculator.html')

@app.route('/fluid-sampling')
def fluid_sampling():
    return render_template('fluid_sampling.html')

# API Endpoints
@app.route('/api/model-options', methods=['GET'])
def model_options():
    """
    Daftar pilihan valid untuk 6 parameter input, diambil langsung dari
    model yang sudah di-training. Dipakai frontend untuk mengisi dropdown.
    """
    return jsonify({
        'success': True,
        'features': MODEL_FEATURES,
        'options': MODEL_OPTIONS,
        # Bagian yang berlaku per jenis peralatan; dipakai frontend menyaring
        # dropdown 'Bagian' setelah jenis peralatan dipilih.
        'part_by_equipment': PART_BY_EQUIPMENT,
        # Tabel kombinasi nyata; dipakai frontend untuk saling menyaring dropdown.
        'master': EQUIPMENT_MASTER,
        # Nilai yang di luar cakupan training tiap model, untuk ditandai di UI.
        'master_unknown_per_model': master_values_unknown_per_model(),
        'models_loaded': {
            'short_term': model_stcr is not None,
            'long_term': model_ltcr is not None
        }
    })


def _extract_features(data):
    """
    Ambil 6 fitur dari payload sebagai string.
    'equipment' diterima sebagai alias lama untuk 'equipment_type'.
    """
    values = {}
    for feature in MODEL_FEATURES:
        raw = data.get(feature)
        if raw is None and feature == 'equipment_type':
            raw = data.get('equipment')
        values[feature] = '' if raw is None else str(raw).strip()
    return values


def _run_prediction(model, known_categories, data):
    """
    Jalankan prediksi memakai 6 fitur kategorikal.

    OneHotEncoder di-training dengan handle_unknown='ignore', jadi nilai di luar
    vocabulary tidak error tapi di-encode sebagai nol (kontribusinya hilang).
    Nilai seperti itu dilaporkan lewat 'unknown_values' supaya hasil yang
    akurasinya menurun tidak lolos tanpa peringatan.

    Bila ada nilai yang asing, angkanya tidak dihitung sama sekali dan hasilnya
    ditandai 'out_of_scope' — lihat penjelasan di dekat MODEL_FEATURES.
    """
    values = _extract_features(data)

    missing = [f for f in MODEL_FEATURES if not values[f]]
    if missing:
        raise ValueError('Parameter wajib belum diisi: ' + ', '.join(missing))

    unknown = {
        feature: values[feature]
        for feature in MODEL_FEATURES
        if known_categories.get(feature) and values[feature] not in known_categories[feature]
    }

    if unknown:
        # Urutkan mengikuti MODEL_FEATURES supaya pesannya konsisten dibaca
        di_luar_cakupan = [f for f in MODEL_FEATURES if f in unknown]
        rincian = ', '.join(f'{f}="{unknown[f]}"' for f in di_luar_cakupan)
        return {
            'success': True,
            'predicted_corrosion_rate': None,
            'out_of_scope': True,
            'out_of_scope_features': di_luar_cakupan,
            'reason': (
                f'{rincian} tidak ada di data training model ini. Nilai asing '
                f'di-encode nol sehingga kontribusinya hilang tanpa jejak — '
                f'angka yang keluar tidak mewakili input yang dipilih, jadi '
                f'prediksi tidak ditampilkan.'
            ),
            'unit': 'mm/year',
            'input': values,
            'unknown_values': unknown,
        }

    # Kolom harus sama persis (nama + urutan) dengan saat training
    input_data = pd.DataFrame([[values[f] for f in MODEL_FEATURES]], columns=MODEL_FEATURES)
    prediction = model.predict(input_data)

    return {
        'success': True,
        'predicted_corrosion_rate': round(float(prediction[0]), 4),
        'out_of_scope': False,
        'unit': 'mm/year',
        'input': values,
        'unknown_values': unknown
    }


@app.route('/api/predict-short-term', methods=['POST'])
def predict_short_term():
    """Predict short-term corrosion rate (STCR p90, XGBoost)"""
    if model_stcr is None:
        return jsonify({
            'success': False,
            'error': 'Model Short-Term belum dimuat atau tidak kompatibel'
        }), 500

    try:
        result = _run_prediction(model_stcr, STCR_CATEGORIES, request.get_json() or {})
        result['model'] = 'STCR p90 (XGBoost)'
        return jsonify(result)
    except ValueError as e:
        return jsonify({'success': False, 'error': str(e)}), 400
    except Exception as e:
        return jsonify({'success': False, 'error': f'{type(e).__name__}: {e}'}), 400


@app.route('/api/predict-long-term', methods=['POST'])
def predict_long_term():
    """Predict long-term corrosion rate (LTCR p50, Random Forest)"""
    if model_ltcr is None:
        return jsonify({
            'success': False,
            'error': 'Model Long-Term belum dimuat atau tidak kompatibel'
        }), 500

    try:
        result = _run_prediction(model_ltcr, LTCR_CATEGORIES, request.get_json() or {})
        result['model'] = 'LTCR p50 (Random Forest)'
        return jsonify(result)
    except ValueError as e:
        return jsonify({'success': False, 'error': str(e)}), 400
    except Exception as e:
        return jsonify({'success': False, 'error': f'{type(e).__name__}: {e}'}), 400

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

@app.route('/api/fluid-model-info', methods=['GET'])
def fluid_model_info():
    """
    Parameter yang dibutuhkan tiap model fluid sampling, dibaca langsung dari
    model terlatih. Frontend memakai ini untuk membangun form sesuai OU terpilih,
    sehingga field otomatis menyesuaikan bila model dilatih ulang.
    """
    models = {}

    for ou, pipeline in FLUID_OU_MODELS.items():
        numeric, equipment_options = get_fluid_model_features(pipeline)
        n = FLUID_TRAIN_SAMPLES.get(ou)
        models[ou] = {
            'label': f'Model khusus {ou}',
            'numeric_features': numeric,
            'equipment_options': equipment_options,
            'needs_equipment': bool(equipment_options),
            'supports_range': True,
            'train_samples': n,
            'quality_note': (
                f'Model {ou} dilatih dari {n} sampel dan cenderung meremehkan '
                f'kasus korosi tinggi. Gunakan sebagai indikasi awal, bukan '
                f'dasar tunggal keputusan inspeksi.'
            ) if n else None,
        }

    if model_fluid is not None:
        models['_default'] = {
            'label': 'Model umum (semua OU lain)',
            'numeric_features': list(FLUID_LEGACY_FEATURES),
            'equipment_options': [],
            'needs_equipment': False,
            'supports_range': False,
            'train_samples': None,
            'quality_note': 'Model umum SVR; tidak menyediakan rentang ketidakpastian.',
        }

    return jsonify({
        'success': True,
        'models': models,
        'ou_with_specific_model': sorted(FLUID_OU_MODELS.keys()),
        'has_default_model': model_fluid is not None,
    })


@app.route('/api/predict-fluid-sampling', methods=['POST'])
def predict_fluid_sampling():
    """
    Prediksi laju korosi dari parameter fluida.

    Model dipilih berdasarkan OU: SLN/SLS memakai model khusus per-OU,
    OU lainnya memakai model umum 'corrosion-rate.pkl' yang tetap dipertahankan.
    """
    try:
        data = request.get_json() or {}
        ou = str(data.get('ou', '')).strip()
        equipment = str(data.get('equipment', '')).strip()
        part = str(data.get('part', '')).strip()

        use_specific = ou in FLUID_OU_MODELS

        if use_specific:
            pipeline = FLUID_OU_MODELS[ou]
            numeric_features, equipment_options = get_fluid_model_features(pipeline)
            required = numeric_features + ['Equipment']
            model_label = f'{ou} (Random Forest, {FLUID_TRAIN_SAMPLES.get(ou, "?")} sampel)'
        else:
            if model_fluid is None:
                return jsonify({
                    'success': False,
                    'error': 'Model Fluid Sampling belum dimuat atau tidak kompatibel'
                }), 500
            pipeline = None
            numeric_features = list(FLUID_LEGACY_FEATURES)
            equipment_options = []
            required = numeric_features
            model_label = 'Umum (SVR 10 fitur)'

        # Kumpulkan nilai: terima nama kolom asli maupun alias snake_case lama
        values = {}
        missing = []
        for feature in numeric_features:
            raw = data.get(feature)
            if raw is None:
                for alias, canonical in FLUID_LEGACY_ALIASES.items():
                    if canonical == feature and data.get(alias) is not None:
                        raw = data.get(alias)
                        break
            if raw is None or str(raw).strip() == '':
                missing.append(feature)
                continue
            try:
                values[feature] = float(raw)
            except (TypeError, ValueError):
                return jsonify({
                    'success': False,
                    'error': f'Nilai "{feature}" harus berupa angka, diterima: {raw!r}'
                }), 400

        if missing:
            return jsonify({
                'success': False,
                'error': 'Parameter wajib belum diisi: ' + ', '.join(missing),
                'missing': missing
            }), 400

        unknown_equipment = None
        if use_specific:
            if not equipment:
                return jsonify({
                    'success': False,
                    'error': 'Parameter wajib belum diisi: Equipment',
                    'missing': ['Equipment']
                }), 400
            if equipment_options and equipment not in equipment_options:
                unknown_equipment = equipment

            row = dict(values)
            row['Equipment'] = equipment
            input_df = pd.DataFrame([[row[f] for f in required]], columns=required)
            prediction, interval = predict_with_interval(pipeline, input_df)
        else:
            # Model lama menerima array polos dengan urutan kolom saat training
            features = np.array([[values[f] for f in numeric_features]])
            prediction = float(model_fluid.predict(features)[0])
            interval = None

        n = FLUID_TRAIN_SAMPLES.get(ou) if use_specific else None
        return jsonify({
            'success': True,
            'predicted_corrosion_rate': round(prediction, 4),
            'range': interval,
            'unit': 'mm/year',
            'model': model_label,
            'model_type': 'ou_specific' if use_specific else 'default',
            'train_samples': n,
            'quality_note': (
                f'Dilatih dari {n} sampel; model cenderung meremehkan kasus '
                f'korosi tinggi. Gunakan sebagai indikasi awal, bukan dasar '
                f'tunggal keputusan inspeksi.'
            ) if n else None,
            'unknown_equipment': unknown_equipment,
            'equipment_info': {'equipment': equipment, 'part': part, 'ou': ou},
            'input': values,
        })
    except Exception as e:
        return jsonify({'success': False, 'error': f'{type(e).__name__}: {e}'}), 400

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
