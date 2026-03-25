from flask import Flask, request, jsonify, render_template
import joblib
import numpy as np

app = Flask(__name__)

# Load model
model = joblib.load('../models/model.pkl')

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

    # temporary feature array (same issue fix)
    features = np.zeros((1, 41))

    features[0][0] = studytime
    features[0][1] = failures
    features[0][2] = absences

    prediction = model.predict(features)

    return render_template('index.html',
                           prediction_text=f"Predicted Score: {prediction[0]:.2f}")

if __name__ == '__main__':
    app.run(debug=True)