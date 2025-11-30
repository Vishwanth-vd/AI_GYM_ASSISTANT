"""
Configuration file for AI Fitness Assistant
"""
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# API Keys
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")

# App Configuration
APP_TITLE = "AI Fitness Assistant 💪"
APP_ICON = "💪"

# File paths
DATA_DIR = "data"
MODELS_DIR = "models"
USER_DATA_DIR = "user_data"

# Create directories if they don't exist
for directory in [DATA_DIR, MODELS_DIR, USER_DATA_DIR]:
    os.makedirs(directory, exist_ok=True)

# Body Fat Calculation Constants
BODY_FAT_FEATURES = ['age', 'weight', 'height', 'neck', 'chest', 'abdomen', 
                      'hip', 'thigh', 'knee', 'ankle', 'biceps', 'forearm', 'wrist']

# Workout Types
WORKOUT_TYPES = ["Strength Training", "Cardio", "HIIT", "Yoga", "Flexibility", "Mixed"]
WORKOUT_LOCATIONS = ["Home", "Gym"]
EXPERIENCE_LEVELS = ["Beginner", "Intermediate", "Advanced"]

# Meal Plan Configuration
MEAL_TYPES = ["Breakfast", "Lunch", "Dinner", "Snacks"]
DIET_PREFERENCES = ["Vegetarian", "Non-Vegetarian", "Vegan", "Eggetarian"]

# Fitness Goals
FITNESS_GOALS = ["Weight Loss", "Muscle Gain", "Maintenance", "Athletic Performance", "General Fitness"]

# Colors for UI
PRIMARY_COLOR = "#FF4B4B"
SECONDARY_COLOR = "#0068C9"
SUCCESS_COLOR = "#09AB3B"
