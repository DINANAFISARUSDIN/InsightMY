from flask import Flask, render_template, request
import pandas as pd
import joblib
import traceback  # Used to print the full error stack trace

app = Flask(__name__)

# Load model and encoder
try:
    preprocessor = joblib.load('models/encoder.pkl')
    model = joblib.load('models/salary_model.pkl')
    print("✅ Model & Encoder loaded successfully!")
except Exception as e:
    print("❌ FAILED TO LOAD MODEL/ENCODER! Please check the 'models' folder.")
    print(str(e))


# ==========================================
#         1. MAIN PAGES (ROUTES)
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
    # Opens the data.html page
    return render_template('data.html')

@app.route('/salary')
def salary_prediction():
    return render_template('salary.html')


# ==========================================
#         2. PREDICTION PROCESS (POST)
# ==========================================

@app.route('/predict', methods=['POST'])
def predict():
    if request.method == 'POST':
        try:
            # 1. Retrieve data from the HTML form
            category = request.form['category']
            job_level = request.form['job_level'] 
            standardized_state = request.form['state']
            min_education = request.form['education']
            
            req_malay = int(request.form.get('req_malay', 0))
            req_english = int(request.form.get('req_english', 0))
            req_mandarin = int(request.form.get('req_mandarin', 0))
            req_japanese = int(request.form.get('req_japanese', 0))

            # 2. Structure data into a pandas DataFrame
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
            
            print("\n--- FORM INPUT DATA ---")
            print(input_data)

            # 3. Transform data using the preprocessor encoder
            X_encoded = preprocessor.transform(input_data)
            
            # 4. Generate predictions from the model
            predictions = model.predict(X_encoded)
            
            print("\n--- MODEL OUTPUT ---")
            print("Output Shape:", predictions.shape if hasattr(predictions, 'shape') else type(predictions))
            print("Output Value:", predictions)

            # 5. Extract prediction values (Handling 1D vs 2D arrays safely)
            if len(predictions.shape) == 2 and predictions.shape[1] >= 2:
                pred_min = round(predictions[0][0], 2)
                pred_max = round(predictions[0][1], 2)
            elif len(predictions.shape) == 1 and len(predictions) >= 2:
                pred_min = round(predictions[0], 2)
                pred_max = round(predictions[1], 2)
            else:
                single_val = predictions[0][0] if len(predictions.shape) == 2 else predictions[0]
                pred_min = round(single_val * 0.85, 2)  # Minimum estimation
                pred_max = round(single_val * 1.15, 2)  # Maximum estimation

            pred_avg = round((pred_min + pred_max) / 2, 2)

            # 6. Send results back to HTML alongside user selections
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
            print("\n❌--- BACKEND ERROR OCCURRED ---❌")
            traceback.print_exc()  # Logs full error traceback to the Render terminal
            return f"<h3>An error occurred in the backend:</h3><p>{str(ralat)}</p><p>Please check the terminal server logs for details.</p>"

if __name__ == "__main__":
    app.run(debug=True)