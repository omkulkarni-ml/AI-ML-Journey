"""
Feature-related API routes.
"""
from flask import Blueprint, jsonify
from ml.features import get_all_features, get_features_by_type, FEATURES, DEFAULT_FEATURES

features_bp = Blueprint('features', __name__)


@features_bp.route('/features', methods=['GET'])
def get_features():
    """
    Get all available features with their metadata.
    
    Returns:
        JSON with all features and their properties
    """
    features = get_all_features()
    
    # Organize features by type
    result = {
        'all_features': features,
        'numeric': get_features_by_type('numeric'),
        'categorical': get_features_by_type('categorical'),
        'default_features': DEFAULT_FEATURES,
        'total_count': len(features)
    }
    
    return jsonify({
        'success': True,
        'data': result
    })


@features_bp.route('/features/numeric', methods=['GET'])
def get_numeric_features():
    """Get only numeric features."""
    return jsonify({
        'success': True,
        'data': get_features_by_type('numeric')
    })


@features_bp.route('/features/categorical', methods=['GET'])
def get_categorical_features():
    """Get only categorical features."""
    return jsonify({
        'success': True,
        'data': get_features_by_type('categorical')
    })


@features_bp.route('/features/defaults', methods=['GET'])
def get_default_features():
    """Get default feature selection."""
    default_info = {}
    for feature in DEFAULT_FEATURES:
        if feature in FEATURES:
            default_info[feature] = FEATURES[feature]
    
    return jsonify({
        'success': True,
        'data': default_info
    })
