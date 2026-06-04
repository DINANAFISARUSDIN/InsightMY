from flask import Flask, render_template, request
import pandas as pd
import joblib
import traceback  # Digunakan untuk print error penuh

app = Flask(__name__)

# Load model dan encoder
try:
    preprocessor = joblib.load('models/encoder.pkl')
    model = joblib.load('models/salary_model.pkl')
    print("✅ Model & Encoder berjaya diload!")
except Exception as e:
    print("❌ GAGAL LOAD MODEL/ENCODER! Sila semak folder 'models'")
    print(str(e))


# ==========================================
#         1. HALAMAN-HALAMAN UTAMA (ROUTES)
# ==========================================

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/data')
def data():
    # Membuka halaman data.html
    return render_template('data.html')

@app.route('/salary')
def salary_prediction():
    return render_template('salary.html')


# ==========================================
#         2. PROSES RAMALAN (PREDICT)
# ==========================================

@app.route('/predict', methods=['POST'])
def predict():
    if request.method == 'POST':
        try:
            # 1. Ambil data dari form HTML
            category = request.form['category']
            job_level = request.form['job_level'] 
            standardized_state = request.form['state']
            min_education = request.form['education']
            
            req_malay = int(request.form.get('req_malay', 0))
            req_english = int(request.form.get('req_english', 0))
            req_mandarin = int(request.form.get('req_mandarin', 0))
            req_japanese = int(request.form.get('req_japanese', 0))

            # 2. Susun data jadi DataFrame
            input_data = pd.DataFrame([{
                'category': category,
                'job_level': job_level,
                'standardized_state': standardized_state,
                'min_education': min_education,
                'req_malay': req_malay,
                'req_english': req_english,
                'req_mandarin': req_mandarin,
                'req_japanese': req_japanese
            }])
            
            print("\n--- DATA INPUT DARI BORANG ---")
            print(input_data)

            # 3. Transform data menggunakan encoder
            X_encoded = preprocessor.transform(input_data)
            
            # 4. Buat ramalan
            predictions = model.predict(X_encoded)
            
            print("\n--- OUTPUT DARI MODEL ---")
            print("Bentuk output (Shape):", predictions.shape if hasattr(predictions, 'shape') else type(predictions))
            print("Nilai output:", predictions)

            # 5. Ekstrak nilai ramalan (Langkah Keselamatan 1D vs 2D array)
            if len(predictions.shape) == 2 and predictions.shape[1] >= 2:
                pred_min = round(predictions[0][0], 2)
                pred_max = round(predictions[0][1], 2)
            elif len(predictions.shape) == 1 and len(predictions) >= 2:
                pred_min = round(predictions[0], 2)
                pred_max = round(predictions[1], 2)
            else:
                single_val = predictions[0][0] if len(predictions.shape) == 2 else predictions[0]
                pred_min = round(single_val * 0.85, 2)  # Anggaran min
                pred_max = round(single_val * 1.15, 2)  # Anggaran max

            pred_avg = round((pred_min + pred_max) / 2, 2)

            # 6. Hantar hasil balik ke HTML berserta maklumat pilihan user
            return render_template('salary.html', 
                                   min_salary=f"{pred_min:,.2f}", 
                                   max_salary=f"{pred_max:,.2f}", 
                                   avg_salary=f"{pred_avg:,.2f}",
                                   sel_category=category,
                                   sel_level=job_level,
                                   sel_state=standardized_state,
                                   sel_education=min_education,
                                   req_malay=req_malay,
                                   req_english=req_english,
                                   req_mandarin=req_mandarin,
                                   req_japanese=req_japanese)

        except Exception as ralat:
            print("\n❌--- RALAT BERLAKU DI BACKEND ---❌")
            traceback.print_exc()  # Log ralat penuh di terminal
            return f"<h3>Aduh! Ada masalah kat backend:</h3><p>{str(ralat)}</p><p>Sila semak log ralat penuh di terminal.</p>"

if __name__ == "__main__":
    app.run(debug=True)