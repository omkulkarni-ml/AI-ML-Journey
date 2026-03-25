"""
Feature definitions and metadata for the student performance model.
"""

FEATURES = {
    # Numeric features
    'age': {
        'type': 'numeric',
        'min': 15,
        'max': 22,
        'description': 'Student age',
        'default': 16
    },
    'Medu': {
        'type': 'numeric',
        'min': 0,
        'max': 4,
        'description': "Mother's education level (0=none, 4=higher education)",
        'default': 2
    },
    'Fedu': {
        'type': 'numeric',
        'min': 0,
        'max': 4,
        'description': "Father's education level (0=none, 4=higher education)",
        'default': 2
    },
    'traveltime': {
        'type': 'numeric',
        'min': 1,
        'max': 4,
        'description': 'Home to school travel time (1=<15min, 4=>1hr)',
        'default': 1
    },
    'studytime': {
        'type': 'numeric',
        'min': 1,
        'max': 4,
        'description': 'Weekly study time (1=<2hr, 4=>10hr)',
        'default': 2
    },
    'failures': {
        'type': 'numeric',
        'min': 0,
        'max': 4,
        'description': 'Number of past class failures',
        'default': 0
    },
    'famrel': {
        'type': 'numeric',
        'min': 1,
        'max': 5,
        'description': 'Family relationship quality (1=very bad, 5=excellent)',
        'default': 4
    },
    'freetime': {
        'type': 'numeric',
        'min': 1,
        'max': 5,
        'description': 'Free time after school (1=very low, 5=very high)',
        'default': 3
    },
    'goout': {
        'type': 'numeric',
        'min': 1,
        'max': 5,
        'description': 'Going out with friends (1=very low, 5=very high)',
        'default': 3
    },
    'Dalc': {
        'type': 'numeric',
        'min': 1,
        'max': 5,
        'description': 'Workday alcohol consumption (1=very low, 5=very high)',
        'default': 1
    },
    'Walc': {
        'type': 'numeric',
        'min': 1,
        'max': 5,
        'description': 'Weekend alcohol consumption (1=very low, 5=very high)',
        'default': 1
    },
    'health': {
        'type': 'numeric',
        'min': 1,
        'max': 5,
        'description': 'Current health status (1=very bad, 5=very good)',
        'default': 3
    },
    'absences': {
        'type': 'numeric',
        'min': 0,
        'max': 93,
        'description': 'School absences (0-93)',
        'default': 0
    },
    'G1': {
        'type': 'numeric',
        'min': 0,
        'max': 20,
        'description': 'First period grade (0-20)',
        'default': 10
    },
    'G2': {
        'type': 'numeric',
        'min': 0,
        'max': 20,
        'description': 'Second period grade (0-20)',
        'default': 10
    },
    # Categorical features
    'school': {
        'type': 'categorical',
        'options': ['GP', 'MS'],
        'description': 'School (GP=Mousinho da Silveira, MS=Miguel Costa)',
        'default': 'GP'
    },
    'sex': {
        'type': 'categorical',
        'options': ['F', 'M'],
        'description': 'Student sex (F=female, M=male)',
        'default': 'F'
    },
    'address': {
        'type': 'categorical',
        'options': ['U', 'R'],
        'description': 'Home address type (U=urban, R=rural)',
        'default': 'U'
    },
    'famsize': {
        'type': 'categorical',
        'options': ['GT3', 'LE3'],
        'description': 'Family size (GT3=greater than 3, LE3=less or equal to 3)',
        'default': 'GT3'
    },
    'Pstatus': {
        'type': 'categorical',
        'options': ['T', 'A'],
        'description': "Parents' cohabitation status (T=together, A=apart)",
        'default': 'T'
    },
    'Mjob': {
        'type': 'categorical',
        'options': ['teacher', 'health', 'services', 'at_home', 'other'],
        'description': "Mother's job",
        'default': 'other'
    },
    'Fjob': {
        'type': 'categorical',
        'options': ['teacher', 'health', 'services', 'at_home', 'other'],
        'description': "Father's job",
        'default': 'other'
    },
    'reason': {
        'type': 'categorical',
        'options': ['home', 'reputation', 'course', 'other'],
        'description': 'Reason to choose school',
        'default': 'course'
    },
    'guardian': {
        'type': 'categorical',
        'options': ['mother', 'father', 'other'],
        'description': 'Student guardian',
        'default': 'mother'
    },
    'schoolsup': {
        'type': 'categorical',
        'options': ['yes', 'no'],
        'description': 'Extra educational support',
        'default': 'no'
    },
    'famsup': {
        'type': 'categorical',
        'options': ['yes', 'no'],
        'description': 'Family educational support',
        'default': 'yes'
    },
    'paid': {
        'type': 'categorical',
        'options': ['yes', 'no'],
        'description': 'Extra paid classes within subject',
        'default': 'no'
    },
    'activities': {
        'type': 'categorical',
        'options': ['yes', 'no'],
        'description': 'Extra-curricular activities',
        'default': 'no'
    },
    'nursery': {
        'type': 'categorical',
        'options': ['yes', 'no'],
        'description': 'Attended nursery school',
        'default': 'yes'
    },
    'higher': {
        'type': 'categorical',
        'options': ['yes', 'no'],
        'description': 'Wants to take higher education',
        'default': 'yes'
    },
    'internet': {
        'type': 'categorical',
        'options': ['yes', 'no'],
        'description': 'Home internet access',
        'default': 'yes'
    },
    'romantic': {
        'type': 'categorical',
        'options': ['yes', 'no'],
        'description': 'With a romantic relationship',
        'default': 'no'
    }
}

# Default features for quick prediction (subset)
DEFAULT_FEATURES = ['studytime', 'failures', 'absences']

# All feature names in order for the original model
ALL_FEATURE_NAMES = [
    'school', 'sex', 'age', 'address', 'famsize', 'Pstatus', 'Medu', 'Fedu',
    'Mjob', 'Fjob', 'reason', 'guardian', 'traveltime', 'studytime', 'failures',
    'schoolsup', 'famsup', 'paid', 'activities', 'nursery', 'higher', 'internet',
    'romantic', 'famrel', 'freetime', 'goout', 'Dalc', 'Walc', 'health', 'absences',
    'G1', 'G2'
]

# Numeric feature names
NUMERIC_FEATURES = [k for k, v in FEATURES.items() if v['type'] == 'numeric']

# Categorical feature names
CATEGORICAL_FEATURES = [k for k, v in FEATURES.items() if v['type'] == 'categorical']


def get_feature_info(feature_name):
    """Get metadata for a specific feature."""
    return FEATURES.get(feature_name, None)


def get_all_features():
    """Get all feature definitions."""
    return FEATURES


def get_features_by_type(feature_type):
    """Get features filtered by type (numeric or categorical)."""
    return {k: v for k, v in FEATURES.items() if v['type'] == feature_type}


def validate_feature_value(feature_name, value):
    """Validate if a value is within acceptable range for a feature."""
    feature = FEATURES.get(feature_name)
    if not feature:
        return False, f"Unknown feature: {feature_name}"
    
    if feature['type'] == 'numeric':
        min_val = feature['min']
        max_val = feature['max']
        try:
            num_value = float(value)
            if num_value < min_val or num_value > max_val:
                return False, f"Value must be between {min_val} and {max_val}"
            return True, ""
        except (ValueError, TypeError):
            return False, "Value must be a number"
    
    elif feature['type'] == 'categorical':
        if value not in feature['options']:
            return False, f"Value must be one of: {', '.join(feature['options'])}"
        return True, ""
    
    return False, "Unknown feature type"
