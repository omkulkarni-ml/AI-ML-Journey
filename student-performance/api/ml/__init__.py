"""
ML module initialization.
"""
from .model import StudentModel, get_model, reload_model
from .features import (
    FEATURES,
    ALL_FEATURE_NAMES,
    NUMERIC_FEATURES,
    CATEGORICAL_FEATURES,
    DEFAULT_FEATURES,
    get_feature_info,
    get_all_features,
    get_features_by_type,
    validate_feature_value
)

__all__ = [
    'StudentModel',
    'get_model',
    'reload_model',
    'FEATURES',
    'ALL_FEATURE_NAMES',
    'NUMERIC_FEATURES',
    'CATEGORICAL_FEATURES',
    'DEFAULT_FEATURES',
    'get_feature_info',
    'get_all_features',
    'get_features_by_type',
    'validate_feature_value'
]
