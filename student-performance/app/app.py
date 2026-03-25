from flask import Flask, request, jsonify, render_template
import joblib
import numpy as np
import pandas as pd

app = Flask(__name__)

# Load model
import os
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
model_path = os.path.join(BASE_DIR, '..', 'models', 'model.pkl')
model = joblib.load(model_path)
columns_path = os.path.join(BASE_DIR, '..', 'models', 'columns.pkl')
columns = joblib.load(columns_path)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict-page')
def predict_page():
    return render_template('predict.html')

@app.route('/predict', methods=['POST'])
def predict():
    studytime = float(request.form['studytime'])
    failures = float(request.form['failures'])
    absences = float(request.form['absences'])

    input_df = pd.DataFrame(columns=columns)
    input_df.loc[0] = 0

    input_df['studytime'] = studytime
    input_df['failures'] = failures
    input_df['absences'] = absences

    prediction = model.predict(input_df)

    return render_template('result.html',
                           prediction=round(prediction[0], 2))

if __name__ == '__main__':
    app.run(debug=True)