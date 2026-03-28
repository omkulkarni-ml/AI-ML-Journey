"""
Model wrapper for the student performance predictor.
"""
import os
import joblib
import pandas as pd

# Get the project root directory (student-performance folder)
# This works regardless of where the script is run from
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# For Render deployment, models are in student-performance/models
# Try multiple paths to find the model files
POSSIBLE_MODEL_PATHS = [
    os.path.join(BASE_DIR, 'models', 'model.pkl'),  # Local development
    os.path.join(BASE_DIR, 'student-performance', 'models', 'model.pkl'),  # Render monorepo
    '/opt/render/project/src/student-performance/models/model.pkl',  # Render absolute path
]

POSSIBLE_COLUMNS_PATHS = [
    os.path.join(BASE_DIR, 'models', 'columns.pkl'),
    os.path.join(BASE_DIR, 'student-performance', 'models', 'columns.pkl'),
    '/opt/render/project/src/student-performance/models/columns.pkl',
]

POSSIBLE_PIPELINE_PATHS = [
    os.path.join(BASE_DIR, 'models', 'pipeline.pkl'),
    os.path.join(BASE_DIR, 'student-performance', 'models', 'pipeline.pkl'),
    '/opt/render/project/src/student-performance/models/pipeline.pkl',
]

def find_existing_file(paths, file_type="file"):
    """Find the first existing file from a list of paths."""
    print(f"Looking for {file_type} in paths: {paths}")
    for path in paths:
        exists = os.path.exists(path)
        print(f"  Checking {path}: {'EXISTS' if exists else 'NOT FOUND'}")
        if exists:
            print(f"Found {file_type} at: {path}")
            return path
    # Log current working directory for debugging
    print(f"Current working directory: {os.getcwd()}")
    print(f"BASE_DIR: {BASE_DIR}")
    # List files in BASE_DIR if it exists
    if os.path.exists(BASE_DIR):
        print(f"Contents of BASE_DIR ({BASE_DIR}):")
        try:
            for item in os.listdir(BASE_DIR):
                print(f"  - {item}")
        except Exception as e:
            print(f"  Error listing BASE_DIR: {e}")
    # Return first path as default (will fail gracefully later)
    return paths[0]

MODEL_PATH = find_existing_file(POSSIBLE_MODEL_PATHS)
COLUMNS_PATH = find_existing_file(POSSIBLE_COLUMNS_PATHS)
PIPELINE_PATH = find_existing_file(POSSIBLE_PIPELINE_PATHS)


class StudentModel:
    """Wrapper class for the student performance prediction model."""

    def __init__(self, model_path=None, pipeline_path=None, columns_path=None):
        """Initialize the model wrapper - lazy loading to save memory."""
        self.model = None
        self.pipeline = None
        self.columns = None
        self._loaded = False
        self._model_path = model_path or MODEL_PATH
        self._pipeline_path = pipeline_path or PIPELINE_PATH
        self._columns_path = columns_path or COLUMNS_PATH
        # Don't load at startup - lazy load on first use

    def _load_model(self, model_path, columns_path):
        """Load the trained model and column names."""
        try:
            self.model = joblib.load(model_path)
            self.columns = joblib.load(columns_path)
        except FileNotFoundError:
            print(f"Warning: Model files not found at {model_path}")
            print("Please run the training notebook first.")
            self.model = None
            self.columns = None

    def _load_pipeline(self, pipeline_path):
        """Load the preprocessing pipeline if available."""
        try:
            self.pipeline = joblib.load(pipeline_path)
        except FileNotFoundError:
            print(f"Warning: Pipeline file not found at {pipeline_path}")
            self.pipeline = None

    def _ensure_loaded(self):
        """Lazy load the model if not already loaded."""
        if not self._loaded:
            print("Lazy loading model...")
            self._load_model(self._model_path, self._columns_path)
            self._load_pipeline(self._pipeline_path)
            self._loaded = True
            print(f"Model loaded: {self.is_loaded()}")

    def is_loaded(self):
        """Check if model is loaded successfully."""
        self._ensure_loaded()
        return self.model is not None and self.columns is not None

    def get_model_info(self):
        """Get model metadata."""
        info = {
            'loaded': self.is_loaded(),
            'model_type': type(self.model).__name__ if self.model else None,
            'n_features': len(self.columns) if self.columns is not None else None,
            'feature_names': list(self.columns) if self.columns is not None else None,
            'has_pipeline': self.pipeline is not None
        }
        return info

    def _get_grade(self, score):
        """Convert numeric score to letter grade."""
        if score >= 16:
            return 'A - Excellent'
        elif score >= 14:
            return 'B - Good'
        elif score >= 12:
            return 'C - Satisfactory'
        elif score >= 10:
            return 'D - Pass'
        elif score >= 8:
            return 'E - Weak Pass'
        else:
            return 'F - Fail'

    def predict(self, input_data, selected_features=None):
        """Make a prediction using selected features."""
        self._ensure_loaded()
        if not self.model or not self.columns:
            return {
                'success': False,
                'error': 'Model not loaded'
            }

        try:
            # Create DataFrame with correct column order
            input_df = pd.DataFrame(columns=self.columns)
            input_df.loc[0] = 0

            # Fill in provided feature values
            for feature, value in input_data.items():
                if feature in input_df.columns:
                    input_df[feature] = value

            # Make prediction
            if self.pipeline:
                prediction = self.pipeline.predict(input_df)
            else:
                prediction = self.model.predict(input_df)

            prediction_value = round(float(prediction[0]), 2)
            confidence = self._calculate_confidence(input_df)
            grade = self._get_grade(prediction_value)

            return {
                'success': True,
                'prediction': prediction_value,
                'grade': grade,
                'confidence_score': confidence,
                'min_score': 0,
                'max_score': 20,
                'unit': 'grade (0-20)',
                'model_version': '1.0.0'
            }

        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }

    def _calculate_confidence(self, input_df):
        """Calculate confidence score based on feature completeness."""
        if self.columns is None:
            return 0.5

        non_default = (input_df.iloc[0] != 0).sum()
        total_features = len(self.columns)

        ratio = non_default / total_features
        confidence = 0.6 + (ratio * 0.35)

        # Convert to Python float for JSON serialization
        return float(round(min(max(confidence, 0.6), 0.95), 2))


_model_instance = None


def get_model():
    """Get or create the singleton model instance."""
    global _model_instance
    if _model_instance is None:
        _model_instance = StudentModel()
    return _model_instance


def reload_model():
    """Force reload the model."""
    global _model_instance
    _model_instance = StudentModel()
    return _model_instance
