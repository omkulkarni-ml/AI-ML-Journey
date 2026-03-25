from flask import Flask, request, jsonify, render_template
import joblib
import numpy as np
import pandas as pd

app = Flask(__name__)

# Load model
model = joblib.load('../models/model.pkl')
columns = joblib.load('../models/columns.pkl')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    data = request.json
    
    # Convert input to array
    features = np.zeros((1, 41))  # match training feature size
    
    prediction = model.predict(features)
    
    return jsonify({
        'prediction': float(prediction[0])
    })

@app.route('/predict_form', methods=['POST'])
def predict_form():

    studytime = int(request.form['studytime'])
    failures = int(request.form['failures'])
    absences = int(request.form['absences'])

    input_df = pd.DataFrame(columns=columns)
    
    # initialize all values to 0
    input_df.loc[0] = 0
   
    # assign user inputs
    input_df['studytime'] = studytime
    input_df['failures'] = failures
    input_df['absences'] = absences

    prediction = model.predict(input_df)

    return render_template('index.html',
                           prediction_text=f"Predicted Score: {prediction[0]:.2f}")

if __name__ == '__main__':
    app.run(debug=True)