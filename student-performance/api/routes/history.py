"""
Prediction history API routes.
"""
from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import db, PredictionHistory, User
from utils.security import require_active_user
from utils.logger import get_logger

history_bp = Blueprint('history', __name__)
logger = get_logger('history')


@history_bp.route('/predictions/history', methods=['GET'])
@jwt_required()
@require_active_user
def get_prediction_history():
    """
    Get prediction history for current user.
    
    Query params:
        page: Page number (default: 1)
        per_page: Items per page (default: 10, max: 50)
        sort_by: Sort field (default: created_at)
        order: Sort order (asc/desc, default: desc)
    """
    try:
        user_id = get_jwt_identity()
        
        # Parse query parameters
        page = request.args.get('page', 1, type=int)
        per_page = min(request.args.get('per_page', 10, type=int), 50)
        sort_by = request.args.get('sort_by', 'created_at')
        order = request.args.get('order', 'desc')
        
        # Validate sort field
        valid_sort_fields = ['created_at', 'prediction_grade', 'confidence_score']
        if sort_by not in valid_sort_fields:
            sort_by = 'created_at'
        
        # Build query
        query = PredictionHistory.query.filter_by(user_id=user_id)
        
        # Apply sorting
        if order == 'desc':
            query = query.order_by(getattr(PredictionHistory, sort_by).desc())
        else:
            query = query.order_by(getattr(PredictionHistory, sort_by).asc())
        
        # Paginate
        pagination = query.paginate(
            page=page,
            per_page=per_page,
            error_out=False
        )
        
        return jsonify({
            'success': True,
            'data': {
                'items': [item.to_dict() for item in pagination.items],
                'pagination': {
                    'page': pagination.page,
                    'per_page': pagination.per_page,
                    'total_pages': pagination.pages,
                    'total_items': pagination.total,
                    'has_next': pagination.has_next,
                    'has_prev': pagination.has_prev
                }
            }
        })
        
    except Exception as e:
        logger.error(f"Get history error: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Failed to fetch prediction history'
        }), 500


@history_bp.route('/predictions/<int:prediction_id>', methods=['GET'])
@jwt_required()
@require_active_user
def get_prediction_detail(prediction_id):
    """Get detailed information about a specific prediction."""
    try:
        user_id = get_jwt_identity()
        
        prediction = PredictionHistory.query.filter_by(
            id=prediction_id,
            user_id=user_id
        ).first()
        
        if not prediction:
            return jsonify({
                'success': False,
                'error': 'Prediction not found'
            }), 404
        
        return jsonify({
            'success': True,
            'data': prediction.to_dict()
        })
        
    except Exception as e:
        logger.error(f"Get prediction detail error: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Failed to fetch prediction details'
        }), 500


@history_bp.route('/predictions/<int:prediction_id>', methods=['DELETE'])
@jwt_required()
@require_active_user
def delete_prediction(prediction_id):
    """Delete a prediction from history."""
    try:
        user_id = get_jwt_identity()
        
        prediction = PredictionHistory.query.filter_by(
            id=prediction_id,
            user_id=user_id
        ).first()
        
        if not prediction:
            return jsonify({
                'success': False,
                'error': 'Prediction not found'
            }), 404
        
        db.session.delete(prediction)
        db.session.commit()
        
        logger.info(f"Prediction {prediction_id} deleted by user {user_id}")
        
        return jsonify({
            'success': True,
            'message': 'Prediction deleted successfully'
        })
        
    except Exception as e:
        db.session.rollback()
        logger.error(f"Delete prediction error: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Failed to delete prediction'
        }), 500


@history_bp.route('/predictions/stats', methods=['GET'])
@jwt_required()
@require_active_user
def get_prediction_stats():
    """Get prediction statistics for current user."""
    try:
        user_id = get_jwt_identity()
        
        # Get total predictions
        total = PredictionHistory.query.filter_by(user_id=user_id).count()
        
        # Get grade distribution
        grade_counts = db.session.query(
            PredictionHistory.prediction_grade,
            db.func.count(PredictionHistory.id)
        ).filter_by(user_id=user_id).group_by(
            PredictionHistory.prediction_grade
        ).all()
        
        grade_distribution = {
            grade: count for grade, count in grade_counts if grade
        }
        
        # Get average confidence
        avg_confidence = db.session.query(
            db.func.avg(PredictionHistory.confidence_score)
        ).filter_by(user_id=user_id).scalar()
        
        # Get predictions by time period (last 30 days)
        from datetime import datetime, timedelta
        thirty_days_ago = datetime.utcnow() - timedelta(days=30)
        recent_count = PredictionHistory.query.filter(
            PredictionHistory.user_id == user_id,
            PredictionHistory.created_at >= thirty_days_ago
        ).count()
        
        return jsonify({
            'success': True,
            'data': {
                'total_predictions': total,
                'recent_predictions': recent_count,
                'grade_distribution': grade_distribution,
                'average_confidence': round(float(avg_confidence), 2) if avg_confidence else None
            }
        })
        
    except Exception as e:
        logger.error(f"Get stats error: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Failed to fetch statistics'
        }), 500
