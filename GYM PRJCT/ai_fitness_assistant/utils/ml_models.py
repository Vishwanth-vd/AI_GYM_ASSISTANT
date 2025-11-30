"""
Machine Learning models for body fat prediction and other features
"""
import numpy as np
from sklearn.linear_model import LinearRegression
import pickle
import os

class BodyFatPredictor:
    """Body fat percentage prediction model"""
    
    def __init__(self):
        self.model = None
        self.is_trained = False
        
    def train_model(self, X, y):
        """Train the body fat prediction model"""
        self.model = LinearRegression()
        self.model.fit(X, y)
        self.is_trained = True
        
    def predict(self, measurements):
        """
        Predict body fat percentage
        measurements: dict with keys like age, weight, height, neck, chest, abdomen, etc.
        """
        if not self.is_trained:
            # Use empirical formula if model not trained
            return self._empirical_prediction(measurements)
        
        # Convert measurements to feature array
        features = self._prepare_features(measurements)
        prediction = self.model.predict([features])[0]
        return max(5.0, min(50.0, prediction))  # Clamp between 5% and 50%
    
    def _empirical_prediction(self, measurements):
        """
        Empirical body fat estimation using Navy Method
        More accurate for general use without training data
        """
        gender = measurements.get('gender', 'male').lower()
        height_cm = measurements.get('height', 170)
        weight_kg = measurements.get('weight', 70)
        waist_cm = measurements.get('abdomen', 85)
        neck_cm = measurements.get('neck', 37)
        
        if gender == 'male':
            # Navy Method for men
            hip_cm = measurements.get('hip', 95)
            body_fat = (495 / (1.0324 - 0.19077 * np.log10(waist_cm - neck_cm) + 
                              0.15456 * np.log10(height_cm))) - 450
        else:
            # Navy Method for women
            hip_cm = measurements.get('hip', 95)
            body_fat = (495 / (1.29579 - 0.35004 * np.log10(waist_cm + hip_cm - neck_cm) + 
                              0.22100 * np.log10(height_cm))) - 450
        
        return max(5.0, min(50.0, body_fat))
    
    def _prepare_features(self, measurements):
        """Prepare feature array from measurements dict"""
        feature_keys = ['age', 'weight', 'height', 'neck', 'chest', 'abdomen', 
                       'hip', 'thigh', 'knee', 'ankle', 'biceps', 'forearm', 'wrist']
        
        features = []
        for key in feature_keys:
            features.append(measurements.get(key, 0))
        
        return np.array(features)
    
    def save_model(self, filepath='models/bodyfat_model.pkl'):
        """Save trained model to file"""
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        with open(filepath, 'wb') as f:
            pickle.dump(self.model, f)
    
    def load_model(self, filepath='models/bodyfat_model.pkl'):
        """Load trained model from file"""
        if os.path.exists(filepath):
            with open(filepath, 'rb') as f:
                self.model = pickle.load(f)
                self.is_trained = True
                return True
        return False

def get_body_fat_category(body_fat_percentage, gender):
    """Categorize body fat percentage"""
    if gender.lower() == 'male':
        if body_fat_percentage < 6:
            return "Essential Fat", "🔵"
        elif 6 <= body_fat_percentage < 14:
            return "Athletes", "🟢"
        elif 14 <= body_fat_percentage < 18:
            return "Fitness", "🟢"
        elif 18 <= body_fat_percentage < 25:
            return "Average", "🟡"
        else:
            return "Obese", "🔴"
    else:  # female
        if body_fat_percentage < 14:
            return "Essential Fat", "🔵"
        elif 14 <= body_fat_percentage < 21:
            return "Athletes", "🟢"
        elif 21 <= body_fat_percentage < 25:
            return "Fitness", "🟢"
        elif 25 <= body_fat_percentage < 32:
            return "Average", "🟡"
        else:
            return "Obese", "🔴"
