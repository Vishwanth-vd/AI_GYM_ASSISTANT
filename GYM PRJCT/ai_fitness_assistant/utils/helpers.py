"""
Helper functions for the AI Fitness Assistant
"""
import json
import os
from datetime import datetime, timedelta
import streamlit as st

def save_user_profile(profile_data):
    """Save user profile to JSON file"""
    user_id = profile_data.get('user_id', 'default_user')
    filepath = f"user_data/{user_id}_profile.json"
    
    with open(filepath, 'w') as f:
        json.dump(profile_data, f, indent=4)
    
    return filepath

def load_user_profile(user_id='default_user'):
    """Load user profile from JSON file"""
    filepath = f"user_data/{user_id}_profile.json"
    
    if os.path.exists(filepath):
        with open(filepath, 'r') as f:
            return json.load(f)
    return None

def save_progress_entry(user_id, progress_data):
    """Save a progress tracking entry"""
    filepath = f"user_data/{user_id}_progress.json"
    
    # Load existing progress
    if os.path.exists(filepath):
        with open(filepath, 'r') as f:
            all_progress = json.load(f)
    else:
        all_progress = []
    
    # Add timestamp
    progress_data['timestamp'] = datetime.now().isoformat()
    all_progress.append(progress_data)
    
    # Save updated progress
    with open(filepath, 'w') as f:
        json.dump(all_progress, f, indent=4)
    
    return filepath

def load_progress_history(user_id='default_user'):
    """Load progress tracking history"""
    filepath = f"user_data/{user_id}_progress.json"
    
    if os.path.exists(filepath):
        with open(filepath, 'r') as f:
            return json.load(f)
    return []

def calculate_bmi(weight_kg, height_cm):
    """Calculate BMI"""
    height_m = height_cm / 100
    bmi = weight_kg / (height_m ** 2)
    return round(bmi, 2)

def get_bmi_category(bmi):
    """Get BMI category"""
    if bmi < 18.5:
        return "Underweight", "🔵"
    elif 18.5 <= bmi < 25:
        return "Normal", "🟢"
    elif 25 <= bmi < 30:
        return "Overweight", "🟡"
    else:
        return "Obese", "🔴"

def calculate_bmr(weight_kg, height_cm, age, gender):
    """Calculate Basal Metabolic Rate using Mifflin-St Jeor Equation"""
    if gender.lower() == 'male':
        bmr = (10 * weight_kg) + (6.25 * height_cm) - (5 * age) + 5
    else:
        bmr = (10 * weight_kg) + (6.25 * height_cm) - (5 * age) - 161
    
    return round(bmr, 2)

def calculate_tdee(bmr, activity_level):
    """Calculate Total Daily Energy Expenditure"""
    activity_multipliers = {
        "Sedentary (little or no exercise)": 1.2,
        "Lightly active (1-3 days/week)": 1.375,
        "Moderately active (3-5 days/week)": 1.55,
        "Very active (6-7 days/week)": 1.725,
        "Super active (athlete)": 1.9
    }
    
    multiplier = activity_multipliers.get(activity_level, 1.2)
    return round(bmr * multiplier, 2)

def predict_transformation_date(current_weight, target_weight, weekly_goal, goal_type):
    """Predict when user will reach their goal"""
    weight_diff = abs(current_weight - target_weight)
    
    # Safe weekly weight change (0.5-1 kg per week)
    if goal_type == "Weight Loss":
        weekly_change = min(abs(weekly_goal), 1.0)
    else:  # Muscle Gain
        weekly_change = min(abs(weekly_goal), 0.5)
    
    weeks_needed = weight_diff / weekly_change if weekly_change > 0 else 0
    days_needed = int(weeks_needed * 7)
    
    target_date = datetime.now() + timedelta(days=days_needed)
    
    return target_date, weeks_needed, days_needed

def format_date(date_obj):
    """Format datetime object to readable string"""
    return date_obj.strftime("%B %d, %Y")

def get_motivational_message(progress_percentage):
    """Get motivational message based on progress"""
    if progress_percentage < 10:
        return "🌱 Every journey begins with a single step. You've got this!"
    elif progress_percentage < 25:
        return "💪 Great start! Keep the momentum going!"
    elif progress_percentage < 50:
        return "🔥 You're making solid progress! Stay consistent!"
    elif progress_percentage < 75:
        return "⭐ Halfway there! Your dedication is paying off!"
    elif progress_percentage < 90:
        return "🚀 Almost there! The finish line is in sight!"
    else:
        return "🏆 Outstanding! You're so close to your goal!"

def init_session_state():
    """Initialize session state variables"""
    if 'user_id' not in st.session_state:
        st.session_state.user_id = 'default_user'
    
    if 'user_profile' not in st.session_state:
        st.session_state.user_profile = load_user_profile(st.session_state.user_id)
    
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
