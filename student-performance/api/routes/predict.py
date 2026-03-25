"""
Prediction API routes.
"""
from flask import Blueprint, jsonify, request
from flask_jwt_extended import get_jwt_identity, verify_jwt_in_request
from ml.model import get_model
from ml.features import validate_feature_value, get_all_features
from models import db, PredictionHistory
from utils.logger import get_logger

predict_bp = Blueprint('predict', __name__)
logger = get_logger('predict')


@predict_bp.route('/predict', methods=['POST'])
def predict():
    """
    Make a prediction based on input features.
    
    Request body:
        {
            "features": {"feature1": value1, ...},
            "selected_features": ["feature1", "feature2", ...] (optional)
        }
    
    Returns:
        JSON with prediction result
    """
    data = request.get_json()
    
    if not data:
        return jsonify({
            'success': False,
            'error': 'No data provided'
        }), 400
    
    features = data.get('features', {}) 
    selected_features = data.get('selected_features')
    
    if not features:
        return jsonify({
            'success': False,
            'error': 'No features provided'
        }), 400
    
    # Validate selected features
    all_features = get_all_features()
    invalid_features = [f for f in features.keys() if f not in all_features]
    if invalid_features:
        return jsonify({
            'success': False,
            'error': f'Invalid features: {invalid_features}'
        }), 400
    
    # Validate feature values
    for feature_name, value in features.items():
        is_valid, error_msg = validate_feature_value(feature_name, value)
        if not is_valid:
            return jsonify({
                'success': False,
                'error': f'Invalid value for {feature_name}: {error_msg}'
            }), 400
    
    # Get model and make prediction
    model = get_model()
    result = model.predict(features, selected_features)
    
    if not result.get('success'):
        return jsonify(result), 500
    
    # Try to save to history if user is authenticated
    try:
        verify_jwt_in_request(optional=True)
        user_id = get_jwt_identity()
        if user_id:
            # Extract grade and confidence from result
            prediction_grade = result.get('grade', '').split()[0] if result.get('grade') else None
            confidence_score = result.get('confidence_score')
            
            history_entry = PredictionHistory(
                user_id=user_id,
                input_features=features,
                selected_features=selected_features,
                prediction_result=result,
                prediction_grade=prediction_grade,
                confidence_score=confidence_score,
                model_version=result.get('model_version', '1.0.0')
            )
            db.session.add(history_entry)
            db.session.commit()
            logger.info(f"Prediction saved to history for user {user_id}")
    except Exception as e:
        # Don't fail the request if history saving fails
        logger.warning(f"Failed to save prediction history: {str(e)}")
        db.session.rollback()
    
    return jsonify({
        'success': True,
        'data': result
    })


@predict_bp.route('/predict/validate', methods=['POST'])
def validate_input():
    """
    Validate input features without making a prediction.
    
    Request body:
        {"features": {"feature1": value1, ...}}
    
    Returns:
        JSON with validation result
    """
    data = request.get_json()
    
    if not data or 'features' not in data:
        return jsonify({
            'success': False,
            'error': 'No features provided'
        }), 400
    
    features = data['features']
    all_features = get_all_features()
    validation_results = {}
    has_errors = False
    
    for feature_name, value in features.items():
        is_valid, error_msg = validate_feature_value(feature_name, value)
        validation_results[feature_name] = {
            'valid': is_valid,
            'error': error_msg if not is_valid else None
        }
        if not is_valid:
            has_errors = True
    
    return jsonify({
        'success': True,
        'data': {
            'is_valid': not has_errors,
            'results': validation_results
        }
    })
