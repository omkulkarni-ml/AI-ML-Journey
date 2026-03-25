"""
Student Performance Predictor - Main Application

This file is kept for backward compatibility.
For the new API structure, see ../api/app.py
"""
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from api.app import app

if __name__ == '__main__':
    app.run(debug=True)