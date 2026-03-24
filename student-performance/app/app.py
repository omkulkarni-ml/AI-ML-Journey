from flask import Flask, request, jsonify
import joblib
import numpy as np

app = Flask(__name__)

# Load model
model = joblib.load('../models/model.pkl')

@app.route('/')
def home():
    return "Student Performance Predictor is running!"

@app.route('/predict', methods=['POST'])
def predict():
    data = request.json
    
    # Convert input to array
    features = np.zeros((1, 41))  # match training feature size
    
    prediction = model.predict(features)
    
    return jsonify({
        'prediction': float(prediction[0])
    })

if __name__ == '__main__':
    app.run(debug=True)