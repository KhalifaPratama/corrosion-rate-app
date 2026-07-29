# Catatan Teknis — Corrosion Rate App

Disusun 29 Juli 2026. Berisi masalah yang perlu ditangani dan hal-hal yang perlu
diketahui saat melanjutkan pengembangan.

---

## Bagian 1 — Masalah yang harus ditangani

Diurutkan dari yang paling mendesak.

### P2. Kualitas model fluid sampling masih lemah

**Status: bug sudah diperbaiki, keterbatasan data belum.**

Bug yang membuat model mengabaikan parameter kimia sudah selesai (lihat
Bagian 3). Namun setelah diperbaiki dan dilatih ulang, kualitas prediksinya
tetap rendah:

| | SLN | SLS |
|---|---|---|
| R² data latih | 0.765 | 0.774 |
| **R² data uji** | **0.038** | **0.222** |
| R² tebak rata-rata | −0.030 | −0.012 |
| MAE uji (mm/year) | 0.0486 | 0.0323 |
| MAE tebak rata-rata | 0.0503 | 0.0387 |

**SLN praktis tidak lebih baik daripada sekadar menebak nilai rata-rata.**
Selisih MAE-nya hanya 3–4%. Jarak lebar antara R² latih dan uji menandakan
model menghafal data latihnya, bukan belajar pola.

Yang lebih perlu diperhatikan, arah kesalahannya konsisten meremehkan:

| OU | Aktual | Prediksi |
|---|---|---|
| SLN | 0.3497 | 0.0703 |
| SLN | 0.1101 | 0.0562 |
| SLS | 0.1732 | 0.0904 |
| SLS | 0.1222 | 0.0492 |

Model paling sering meleset justru pada kasus korosi tinggi — kasus yang paling
penting terdeteksi. Untuk aplikasi integritas aset, ini arah kesalahan yang
paling tidak diinginkan.

Akar masalahnya bukan algoritma, melainkan jumlah data: **64 baris (SLN) dan
37 baris (SLS) untuk 10 fitur**. SLS hanya menyisakan 8 baris untuk pengujian,
sehingga angka akurasinya sendiri tidak stabil.

Yang perlu dilakukan:

1. Menambah jumlah data sampling. Ini yang paling berdampak — jauh melebihi
   efek mengganti algoritma atau menyetel hyperparameter.
2. Selama data masih sedikit, pertahankan tampilan rentang ketidakpastian dan
   catatan keterbatasan di UI (sudah terpasang).
3. Pertimbangkan `cross_val_score` (misal 5-fold) sebagai pengganti satu kali
   `train_test_split`, karena pada data sekecil ini satu split saja terlalu
   bergantung pada keberuntungan pembagian.

---

### P3. Postur risiko tidak konsisten antara short-term dan long-term

**Status: perlu keputusan engineering, bukan keputusan teknis.**

Kedua model corrosion calculator memakai target yang berbeda tingkat
konservatismenya:

| Model | Target | Arti |
|---|---|---|
| `model - stcr.joblib` | `str_p90` | persentil ke-90 (konservatif) |
| `model - ltcr.joblib` | `ltr_p50` | median (moderat) |

Artinya kartu hasil menampilkan dua angka berdampingan yang berasal dari dua
asumsi risiko berbeda. Untuk perhitungan sisa umur dan interval inspeksi,
perbedaan ini berpengaruh langsung.

Kolom `ltr_p90` **sudah tersedia di dataset** — notebook justru membuangnya di
`drop_cols`. Jadi kalau diputuskan long-term perlu konservatif juga, ubah satu
baris di `model - ltcr - p50_random forest.ipynb`:

```python
y = ltcr_filter['ltr_p90']   # dari 'ltr_p50'
```

Keputusan p50 atau p90 sebaiknya dikonfirmasi ke engineer integritas, karena
menentukan seberapa konservatif rekomendasi inspeksi yang dihasilkan.

---

### P3b. Cakupan data STCR jauh lebih sempit daripada LTCR

**Status: dampaknya sudah ditandai di UI, akar masalahnya belum diperbaiki.**

Kedua model corrosion calculator memakai 6 fitur yang sama, tetapi dilatih pada
data dengan cakupan yang sangat berbeda:

| Fitur | Dikenal STCR | Dikenal LTCR |
|---|---|---|
| equipment_type | 3 — **FFC tidak ada sama sekali** | 4 |
| facility | 91 | 191 |
| category | 33 | 48 |
| asset_owner | 11 | 16 |

Karena `handle_unknown='ignore'`, nilai di luar cakupan tidak menimbulkan error
tetapi di-encode nol sehingga kontribusinya hilang. Akibatnya untuk sebagian
peralatan yang benar-benar ada di lapangan, **angka short-term jauh kurang dapat
dipercaya daripada long-term**, padahal keduanya ditampilkan berdampingan
seolah setara.

Dari 901 kombinasi di `equipment_master.json`, ada **119 nilai** yang di luar
cakupan salah satu model — 118 di antaranya milik STCR (96 facility, 16
category, 5 asset_owner, 1 equipment_type), dan hanya 1 milik LTCR
(`Water Seal`).

Penanganan sementara: nilai seperti itu diberi tanda `⚠ short-term kurang
akurat` langsung di dropdown, sehingga terlihat sebelum menekan Hitung, bukan
baru diketahui setelah hasil keluar.

Yang perlu dilakukan: latih ulang STCR memakai cakupan data seluas LTCR.
Perbaikan ini sekaligus menghapus seluruh 119 penanda tersebut. Perlu ditelusuri
lebih dulu mengapa data training short-term jauh lebih sedikit — apakah memang
pengukuran short-term belum tersedia untuk fasilitas-fasilitas itu, atau ada
penyaringan yang tidak disengaja saat menyiapkan data.

Catatan: selama FFC belum dikenal STCR, jenis peralatan itu tetap ditampilkan
(peralatannya nyata ada) tetapi angka short-term-nya perlu diperlakukan sebagai
indikasi kasar saja.

---

### P4. Model umum fluid sampling (`corrosion-rate.pkl`) belum tervalidasi

**Status: masih dipakai untuk OU HO, HCT, FM, PGT.**

Model ini berupa `SVR` polos tanpa penskalaan fitur. Akibatnya fitur bernilai
besar mendominasi, sementara fitur bernilai kecil nyaris tidak berpengaruh.
Terlihat dari uji sensitivitas:

```
Resistivity  diubah -> delta +0.018469   (paling dominan)
Salinity     diubah -> delta -0.012077
pH           diubah -> delta -0.000000   (nyaris tidak berpengaruh)
SO4          diubah -> delta -0.000001
```

pH yang tidak berpengaruh sulit dibenarkan secara kimia untuk prediksi korosi.
Model ini juga tidak punya metrik akurasi yang terdokumentasi, dan dilatih
dengan scikit-learn versi lama (memunculkan `InconsistentVersionWarning` saat
dimuat).

Yang perlu dilakukan: latih ulang dengan `StandardScaler` di dalam pipeline dan
ukur akurasinya, atau buat model khusus untuk OU-OU tersebut seperti SLN/SLS.

---

### P5. Model corrosion calculator lama menghasilkan nilai mustahil

**Status: sudah tidak dipakai aplikasi, file masih ada di disk.**

`model_str.joblib` dan `model_ltr.joblib` sudah digantikan model 6-fitur.
Keduanya sebaiknya tidak dihidupkan kembali, karena:

- Mengeluarkan **laju korosi negatif** (Pressure Vessel −0.0581, FFC −0.0934
  mm/year) — mustahil secara fisika. Notebook lama tidak memfilter nilai negatif,
  notebook baru memfilternya.
- Mengeluarkan nilai ekstrem tidak wajar (5.5154 mm/year, ±35× lipat model baru).
- Menerima input tak dikenal secara diam-diam tanpa peringatan.
- **Tidak pernah divalidasi**: notebooknya meng-`import train_test_split` tetapi
  tidak pernah memakainya — `fit()` dijalankan pada 100% data. Dikombinasi dengan
  `TargetEncoder` yang rawan kebocoran target, akurasinya tidak pernah terukur.

Yang perlu dilakukan: arsipkan atau hapus supaya tidak terpakai tidak sengaja.

---

### P6. Template mati

`templates/short_termOLD.html`, `templates/long_termOLD.html`, dan
`templates/fluid_samplingOLD.html` tidak punya route di `app.py` sehingga tidak
pernah tampil. Dua yang pertama masih memakai kontrak API lama (3 field).
Sebaiknya dihapus agar tidak membingungkan.

---

## Bagian 2 — Hal yang perlu diketahui

### Menjalankan aplikasi

Gunakan `RUN_APP.bat`. Sempat gagal dengan `ModuleNotFoundError: No module named
'flask'` karena folder proyek pernah dipindah dari `D:\...\magangG8\nano\...`
ke lokasi sekarang, sementara `test_env\Scripts\activate.bat` masih menyimpan
path lama secara hardcoded. Sudah diperbaiki.

**Pelajaran:** virtual environment Python menyimpan path absolut. Kalau folder
proyek dipindah lagi, `test_env` akan rusak lagi. Cara paling bersih adalah
membuat ulang venv setelah pindah, bukan menyunting path-nya.

### Menjalankan notebook

Pakai kernel **`Python (test_env - kalkulator CR)`**, bukan `.venv`.

`.venv` (Python 3.14, dibuat otomatis oleh editor) hanya berisi `ipykernel` —
itu penyebab error `No module named joblib`. Boleh dihapus kalau tidak dipakai.

Alasan memakai `test_env`: model harus dilatih dengan versi library yang sama
dengan yang memuatnya di aplikasi. Kalau berbeda, muncul
`InconsistentVersionWarning` dan hasil prediksi berpotensi tidak konsisten.

### Dependensi

`requirements.txt` sengaja hanya memuat kebutuhan aplikasi berjalan.
Paket khusus training **tidak** dimasukkan agar deployment tidak membengkak:

```
openpyxl      # baca data.xlsx
matplotlib    # plot EDA di notebook
seaborn       # plot EDA di notebook
nbconvert     # menjalankan notebook dari terminal
```

Semuanya sudah terpasang di `test_env`. `xgboost` masuk `requirements.txt`
karena dibutuhkan aplikasi untuk memuat `model - stcr.joblib`.

### Cara form tersambung ke model

Form **tidak** memuat daftar pilihan atau nama field secara hardcoded. Server
membacanya langsung dari model terlatih:

- `/api/model-options` — kategori tiap fitur, diambil dari `OneHotEncoder`
  hasil training (corrosion calculator).
- `/api/fluid-model-info` — daftar fitur tiap model, diambil dari
  `pipeline.feature_names_in_` (fluid sampling).

Konsekuensinya: **kalau model dilatih ulang dan fiturnya berubah, form ikut
menyesuaikan otomatis** tanpa mengubah kode. Ini penting karena `SelectKBest`
memang bisa memilih fitur berbeda bila datanya bertambah.

### Pemilihan model fluid sampling

| OU | Model |
|---|---|
| SLN | `model - fluid sampling - SLN.joblib` |
| SLS | `model - fluid sampling - SLS.joblib` |
| HO, HCT, FM, PGT | `corrosion-rate.pkl` (umum) |

Model umum tetap dipertahankan karena model khusus hanya mencakup 2 dari 6 OU.

### Vocabulary model corrosion calculator berbeda

Model STCR dilatih pada data lebih sempit daripada LTCR:

| Fitur | STCR | LTCR |
|---|---|---|
| facility | 91 | 191 |
| category | 33 | 48 |
| asset_owner | 11 | 16 |

Karena `handle_unknown='ignore'`, nilai di luar vocabulary tidak menimbulkan
error tetapi di-encode nol sehingga kontribusinya hilang. Agar tidak lolos tanpa
disadari, API mengembalikan `unknown_values` dan UI menampilkannya sebagai
peringatan. Dropdown diisi gabungan kedua model.

### Penamaan file model

Notebook fluid sampling kini menyimpan langsung dengan nama yang dipakai proyek
(`model - fluid sampling - SLN.joblib`). Sebelumnya menyimpan sebagai
`model - SLN.joblib` sehingga perlu rename manual — sumber kesalahan yang mudah
terlewat.

### Berkas backup

Boleh dihapus setelah yakin tidak ada masalah:

```
model - fluid sampling - SLN.joblib.old    model lama sebelum perbaikan
model - fluid sampling - SLS.joblib.old
model - fluid sampling - SLN.ipynb.bak     notebook sebelum disunting
model - fluid sampling - SLS.ipynb.bak
```

---

## Bagian 3 — Yang sudah diperbaiki

### Virtual environment rusak setelah folder dipindah

`activate.bat` dan `activate` masih menunjuk path lama. Diperbaiki ke path
sekarang; `RUN_APP.bat` berjalan normal kembali.

### Corrosion calculator beralih ke model 6 fitur

Dari `equipment, part, ou` (3 fitur) menjadi `equipment_type, category, part,
asset_owner, ou, facility` (6 fitur), memakai `model - stcr.joblib` dan
`model - ltcr.joblib`.

Diverifikasi: 12 kombinasi acak × 2 endpoint, **24/24 hasil API identik** dengan
memanggil model langsung.

Sekalian diperbaiki: sisa umur bernilai `Infinity` saat laju korosi nol, dan
presisi tampilan dinaikkan ke 4 desimal (nilai prediksi berkisar 0.02–0.2,
pada 3 desimal presisinya terbuang).

### Model fluid sampling mengabaikan seluruh parameter kimia

Bug paling serius yang ditemukan. `ColumnTransformer` hanya mendefinisikan
transformer untuk `Equipment`, sedangkan **default `remainder` adalah `'drop'`**,
sehingga 10 kolom kimia dibuang sebelum sampai ke regressor.

Akibatnya tiap model hanya bisa mengeluarkan 2 nilai berbeda — praktis tabel
lookup, bukan model. Tidak memunculkan error apa pun sehingga lolos tanpa
disadari.

```python
# Sebelum — 10 kolom kimia terbuang diam-diam
preprocessor = ColumnTransformer(
    transformers=[('cat', OneHotEncoder(handle_unknown='ignore'), categorical_cols)]
)

# Sesudah
preprocessor = ColumnTransformer(
    transformers=[('cat', OneHotEncoder(handle_unknown='ignore'), categorical_cols)],
    remainder='passthrough'
)
```

Setelah diperbaiki dan dilatih ulang: SLN 10 dari 10 parameter berpengaruh,
SLS 9 dari 10 (`Sr` kebetulan tidak dipakai Random Forest sebagai pemecah cabang).

Catatan: model `stcr`/`ltcr` lolos dari bug yang sama hanya karena keenam
fiturnya kategorikal, sehingga `remainder` tidak punya apa-apa untuk dibuang.
Di fluid sampling, 10 dari 11 fitur bersifat numerik.

### Hasil training tidak reproducible

`SelectKBest` dan `RandomForestRegressor` tidak diberi `random_state`, sehingga
tiap kali notebook dijalankan bisa menghasilkan set fitur yang berbeda — terbukti
saat `pH` tergantikan `Na` di SLN dan `M-Alkalinity` tergantikan `HCO3` di SLS
padahal datanya sama.

```python
from functools import partial
selector = SelectKBest(score_func=partial(mutual_info_regression, random_state=42), k=10)
('regressor', RandomForestRegressor(random_state=42))
```

Diverifikasi dengan melatih ulang dua kali: fitur terpilih dan prediksi identik
sampai 10 desimal.

**Implikasi yang perlu diingat:** sebagian perbedaan fitur antara SLN dan SLS
kemungkinan hanya derau seleksi pada data kecil, bukan perbedaan fisik nyata
antar operating unit.

### Sumber data notebook

Sel 0 semula membaca `/Samsudiat/NANO/model-corrosion-rate/Juli 2026/data.xlsx`,
lokasi yang hanya ada di komputer pembuat notebook. Kini diarahkan ke
`data.xlsx` di folder proyek.

### Integrasi fluid sampling per-OU

Form membangun field mengikuti OU terpilih, menampilkan rentang ketidakpastian
(persentil 10–90 dari sebaran antar-pohon Random Forest), nama model yang
dipakai, serta catatan keterbatasan.

Diverifikasi: 8 uji model per-OU + 4 uji model umum + kompatibilitas alias lama
+ validasi input + Equipment tak dikenal — **seluruhnya lolos, 0 gagal**.

---

## Ringkasan prioritas

| # | Masalah | Tindakan |
|---|---|---|
| P2 | Data fluid sampling terlalu sedikit | Tambah sampel |
| P3 | p90 vs p50 tidak konsisten | Putuskan bersama engineer integritas |
| P3b | Cakupan data STCR jauh lebih sempit | Latih ulang STCR seluas LTCR |
| P4 | SVR umum tanpa scaling | Latih ulang dengan `StandardScaler` |
| P5 | Model lama bernilai mustahil | Arsipkan atau hapus |
| P6 | Template mati | Hapus |

