"""
AI Fitness Assistant - Single Page Application
A comprehensive fitness tracking and planning application with AI-powered features.
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime
import json

# Import utility modules
from utils.helpers import (
    init_session_state, save_user_profile, load_user_profile,
    calculate_bmi, get_bmi_category, calculate_bmr, calculate_tdee,
    save_progress_entry, load_progress_history,
    predict_transformation_date, format_date, get_motivational_message
)
from utils.ml_models import BodyFatPredictor, get_body_fat_category
from utils.workout_generator import WorkoutGenerator
from utils.meal_planner import MealPlanner
from utils.ai_coach import AICoach
from config import (
    FITNESS_GOALS, EXPERIENCE_LEVELS, WORKOUT_TYPES, WORKOUT_LOCATIONS,
    DIET_PREFERENCES, GEMINI_API_KEY
)


# ============================================================================
# PAGE CONFIGURATION
# ============================================================================

st.set_page_config(
    page_title="AI Fitness Assistant",
    page_icon="💪",
    layout="wide",
    initial_sidebar_state="collapsed"
)


# ============================================================================
# CUSTOM CSS STYLING
# ============================================================================

def load_custom_styles():
    """Load custom CSS for premium UI design."""
    st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&family=Montserrat:wght@400;500;600;700;800;900&display=swap');
        
        /* Global Styles with Professional Fonts */
        * { 
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
        }
        
        h1, h2, h3, h4, h5, h6 {
            font-family: 'Montserrat', sans-serif !important;
            font-weight: 800 !important;
            letter-spacing: -0.5px;
        }
        
        /* Animated Gradient Background */
        .stApp {
            background: linear-gradient(-45deg, #667eea, #764ba2, #f093fb, #4facfe);
            background-size: 400% 400%;
            animation: gradientBG 20s ease infinite;
        }
        
        @keyframes gradientBG {
            0% { background-position: 0% 50%; }
            50% { background-position: 100% 50%; }
            100% { background-position: 0% 50%; }
        }
        
        /* Main Container with Enhanced Glassmorphism */
        .main .block-container {
            background: rgba(255, 255, 255, 0.15);
            backdrop-filter: blur(20px) saturate(180%);
            border-radius: 25px;
            padding: 2.5rem;
            box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.4);
            border: 1px solid rgba(255, 255, 255, 0.25);
        }
        
        /* Modern Tab Styling */
        .stTabs [data-baseweb="tab-list"] {
            gap: 12px;
            background: rgba(255, 255, 255, 0.15);
            backdrop-filter: blur(10px);
            padding: 12px;
            border-radius: 20px;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
        }
        
        .stTabs [data-baseweb="tab"] {
            background: rgba(255, 255, 255, 0.25);
            border-radius: 12px;
            padding: 12px 24px;
            font-weight: 600;
            font-size: 0.95rem;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            border: 1px solid rgba(255, 255, 255, 0.2);
            color: rgba(0, 0, 0, 0.7);
        }
        
        .stTabs [data-baseweb="tab"]:hover {
            background: rgba(255, 255, 255, 0.35);
            transform: translateY(-2px);
        }
        
        .stTabs [aria-selected="true"] {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
            color: white !important;
            box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4);
            transform: translateY(-2px);
        }
        
        /* Enhanced Button Styling */
        .stButton>button {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            border-radius: 16px;
            padding: 0.85rem 2.5rem;
            font-weight: 700;
            font-size: 1rem;
            letter-spacing: 0.3px;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            box-shadow: 0 6px 24px rgba(102, 126, 234, 0.35);
            position: relative;
            overflow: hidden;
        }
        
        .stButton>button::before {
            content: '';
            position: absolute;
            top: 0;
            left: -100%;
            width: 100%;
            height: 100%;
            background: linear-gradient(90deg, transparent, rgba(255,255,255,0.3), transparent);
            transition: left 0.5s;
        }
        
        .stButton>button:hover::before {
            left: 100%;
        }
        
        .stButton>button:hover {
            transform: translateY(-3px) scale(1.02);
            box-shadow: 0 12px 35px rgba(102, 126, 234, 0.5);
        }
        
        /* Premium Metric Cards */
        .metric-card {
            background: rgba(255, 255, 255, 0.95);
            backdrop-filter: blur(10px);
            padding: 2rem;
            border-radius: 24px;
            box-shadow: 0 15px 35px rgba(0,0,0,0.1);
            transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
            border: 1px solid rgba(255, 255, 255, 0.6);
            position: relative;
            overflow: hidden;
            color: #333333 !important;
        }
        
        .metric-card::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 6px;
            background: linear-gradient(90deg, #ff6b35, #f7931e, #ff6b35);
            background-size: 200% 100%;
            animation: shimmer 3s linear infinite;
        }
        
        @keyframes shimmer {
            0% { background-position: -200% 0; }
            100% { background-position: 200% 0; }
        }
        
        .metric-card:hover {
            transform: translateY(-8px) scale(1.01);
            box-shadow: 0 20px 50px rgba(255, 107, 53, 0.15);
            border-color: rgba(255, 107, 53, 0.3);
        }
        
        .metric-card h3 {
            color: #ff6b35 !important;
            font-size: 1.6rem;
            margin-bottom: 1.2rem;
            font-weight: 900;
            text-transform: uppercase;
            letter-spacing: 1px;
        }
        
        .metric-card ul, .metric-card ol {
            margin: 0;
            padding-left: 1.5rem;
            color: #444444 !important;
        }
        
        .metric-card li {
            margin-bottom: 0.8rem;
            font-size: 1rem;
            line-height: 1.7;
            color: #444444 !important;
        }
        
        /* Streamlit Metric Enhancement */
        .stMetric {
            background: linear-gradient(145deg, #ffffff, #f5f5f7);
            padding: 1.5rem;
            border-radius: 20px;
            box-shadow: 
                0 10px 25px rgba(0,0,0,0.05),
                inset 0 0 0 1px rgba(255,255,255,1);
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            position: relative;
            overflow: hidden;
            border: 1px solid rgba(0,0,0,0.05);
        }
        
        .stMetric::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 5px;
            background: linear-gradient(90deg, #ff6b35, #f7931e);
            opacity: 0.8;
        }
        
        .stMetric label {
            color: #666666 !important;
            font-weight: 600 !important;
            font-size: 0.9rem !important;
            text-transform: uppercase;
            letter-spacing: 1px;
        }
        
        .stMetric [data-testid="stMetricValue"] {
            color: #333333 !important;
            font-weight: 800 !important;
            font-size: 2rem !important;
            font-family: 'Bebas Neue', sans-serif !important;
        }
        
        .stMetric:hover {
            transform: translateY(-5px);
            box-shadow: 0 15px 35px rgba(255, 107, 53, 0.15);
            border-color: rgba(255, 107, 53, 0.3);
        }
        
        /* Form Styling */
        .stTextInput>div>div>input,
        .stNumberInput>div>div>input,
        .stSelectbox>div>div>div,
        .stTextArea>div>div>textarea {
            border-radius: 12px;
            border: 2px solid rgba(102, 126, 234, 0.2);
            padding: 0.75rem 1rem;
            font-size: 0.95rem;
            transition: all 0.3s ease;
        }
        
        .stTextInput>div>div>input:focus,
        .stNumberInput>div>div>input:focus,
        .stTextArea>div>div>textarea:focus {
            border-color: #667eea;
            box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
        }
        
        /* Info/Success/Warning Boxes */
        .stAlert {
            border-radius: 14px;
            border: none;
            backdrop-filter: blur(10px);
            font-weight: 500;
        }
        
        /* Expander Styling */
        .streamlit-expanderHeader {
            background: rgba(255, 255, 255, 0.9);
            border-radius: 12px;
            font-weight: 600;
            padding: 1rem;
            transition: all 0.3s ease;
        }
        
        .streamlit-expanderHeader:hover {
            background: rgba(255, 255, 255, 1);
            box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        }
        
        /* Progress Bar */
        .stProgress > div > div > div > div {
            background: linear-gradient(90deg, #667eea, #764ba2);
            border-radius: 10px;
        }
        
        /* Custom Scrollbar */
        ::-webkit-scrollbar {
            width: 12px;
            height: 12px;
        }
        
        ::-webkit-scrollbar-track {
            background: rgba(255, 255, 255, 0.1);
            border-radius: 10px;
        }
        
        ::-webkit-scrollbar-thumb {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            border-radius: 10px;
            border: 2px solid rgba(255, 255, 255, 0.2);
        }
        
        ::-webkit-scrollbar-thumb:hover {
            background: linear-gradient(135deg, #764ba2 0%, #667eea 100%);
        }
        
        /* Chat Message Styling */
        .chat-message {
            padding: 1.25rem;
            border-radius: 16px;
            margin: 0.75rem 0;
            font-size: 0.95rem;
            line-height: 1.6;
            box-shadow: 0 2px 10px rgba(0,0,0,0.08);
        }
        </style>
    """, unsafe_allow_html=True)


# ============================================================================
# HELPER FUNCTIONS FOR UI COMPONENTS
# ============================================================================

def render_header():
    """Render the main application header."""
    st.markdown("""
        <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    padding: 2.5rem 2rem; border-radius: 24px; text-align: center;
                    margin-bottom: 2rem; box-shadow: 0 12px 48px rgba(102, 126, 234, 0.5);
                    border: 1px solid rgba(255, 255, 255, 0.2);">
            <h1 style="color: white !important; margin: 0; font-size: 3.5rem; 
                       font-weight: 900; text-shadow: 2px 2px 8px rgba(0,0,0,0.2);
                       background: none !important; -webkit-text-fill-color: white !important;">
                💪 AI FITNESS ASSISTANT
            </h1>
            <p style="color: rgba(255, 255, 255, 0.95) !important; 
                      margin: 1rem 0 0 0; font-size: 1.25rem; font-weight: 500;
                      letter-spacing: 0.5px; text-shadow: 1px 1px 4px rgba(0,0,0,0.1);">
                Your Personal AI-Powered Fitness & Nutrition Coach
            </p>
        </div>
    """, unsafe_allow_html=True)


def validate_profile_data(name, age, weight, height, goal_weight):
    """Validate user profile input data."""
    errors = []
    
    if not name or len(name.strip()) == 0:
        errors.append("Name cannot be empty")
    if age < 15 or age > 100:
        errors.append("Age must be between 15 and 100")
    if weight < 30 or weight > 200:
        errors.append("Weight must be between 30 and 200 kg")
    if height < 100 or height > 250:
        errors.append("Height must be between 100 and 250 cm")
    if goal_weight < 30 or goal_weight > 200:
        errors.append("Goal weight must be between 30 and 200 kg")
    
    return errors


# ============================================================================
# TAB CONTENT FUNCTIONS
# ============================================================================

def render_home_tab():
    """Render the home/dashboard tab."""
    st.markdown("## 🏠 Welcome to Your Fitness Journey!")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
            <div class="metric-card" style="color: #333;">
                <h3 style="color: #667eea;">🎯 What We Offer</h3>
                <ul style="color: #333; line-height: 1.8;">
                    <li>📊 <b>Body Fat Analysis</b> - Accurate composition tracking</li>
                    <li>💪 <b>Workout Plans</b> - Personalized for home or gym</li>
                    <li>🍽️ <b>Meal Planning</b> - Indian cuisine nutrition</li>
                    <li>🤖 <b>AI Coach</b> - 24/7 fitness guidance</li>
                    <li>📈 <b>Progress Tracking</b> - Monitor transformation</li>
                    <li>🎯 <b>Goal Prediction</b> - Know when you'll reach targets</li>
                </ul>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
            <div class="metric-card" style="color: #333;">
                <h3 style="color: #667eea;">🚀 Getting Started</h3>
                <ol style="color: #333; line-height: 1.8;">
                    <li>📝 <b>Create Your Profile</b> - Go to User Profile tab</li>
                    <li>📊 <b>Check Body Fat</b> - Use our calculator</li>
                    <li>💪 <b>Get Workout Plan</b> - Generate daily workouts</li>
                    <li>🍽️ <b>Plan Your Meals</b> - Get nutrition guidance</li>
                    <li>🤖 <b>Chat with AI Coach</b> - Ask anything!</li>
                    <li>📈 <b>Track Progress</b> - Log your journey</li>
                </ol>
            </div>
        """, unsafe_allow_html=True)
    
    # Display user stats if profile exists
    user_profile = st.session_state.get('user_profile')
    if user_profile:
        st.markdown("## 📊 Your Quick Stats")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Current Weight", f"{user_profile.get('weight', 'N/A')} kg")
        with col2:
            st.metric("Goal Weight", f"{user_profile.get('goal_weight', 'N/A')} kg")
        with col3:
            st.metric("Height", f"{user_profile.get('height', 'N/A')} cm")
        with col4:
            st.metric("Goal", user_profile.get('goal', 'N/A'))
    else:
        st.info("👋 **New Here?** Start by creating your profile in the User Profile tab!")


def render_profile_tab():
    """Render the user profile tab."""
    st.markdown("## 👤 User Profile")
    st.markdown("Create and manage your fitness profile")
    
    # Load existing profile
    if 'user_profile' not in st.session_state:
        st.session_state.user_profile = load_user_profile()
    
    profile = st.session_state.user_profile or {}
    
    with st.form("profile_form"):
        st.subheader("📝 Personal Information")
        
        col1, col2 = st.columns(2)
        
        with col1:
            name = st.text_input("Name", value=profile.get('name', ''))
            age = st.number_input("Age", 15, 100, int(profile.get('age', 25)))
            gender = st.selectbox("Gender", ["Male", "Female"], 
                                 index=0 if profile.get('gender', 'Male') == 'Male' else 1)
            height = st.number_input("Height (cm)", 100, 250, int(profile.get('height', 170)))
        
        with col2:
            weight = st.number_input("Current Weight (kg)", 30.0, 200.0, 
                                    float(profile.get('weight', 70.0)), 0.1)
            goal_weight = st.number_input("Goal Weight (kg)", 30.0, 200.0,
                                         float(profile.get('goal_weight', 65.0)), 0.1)
            goal = st.selectbox("Fitness Goal", FITNESS_GOALS,
                               index=FITNESS_GOALS.index(profile.get('goal', 'Weight Loss'))
                               if profile.get('goal') in FITNESS_GOALS else 0)
            experience = st.selectbox("Experience Level", EXPERIENCE_LEVELS,
                                     index=EXPERIENCE_LEVELS.index(profile.get('experience', 'Beginner'))
                                     if profile.get('experience') in EXPERIENCE_LEVELS else 0)
        
        st.subheader("🏃 Activity Level")
        activity_options = [
            "Sedentary (little or no exercise)",
            "Lightly active (1-3 days/week)",
            "Moderately active (3-5 days/week)",
            "Very active (6-7 days/week)",
            "Super active (athlete)"
        ]
        activity_level = st.select_slider("How active are you?", activity_options,
                                         value=profile.get('activity_level', activity_options[2]))
        
        st.subheader("🍽️ Diet Preferences")
        diet_preference = st.selectbox("Diet Type", DIET_PREFERENCES,
                                      index=DIET_PREFERENCES.index(profile.get('diet_preference', 'Vegetarian'))
                                      if profile.get('diet_preference') in DIET_PREFERENCES else 0)
        
        submitted = st.form_submit_button("💾 Save Profile", use_container_width=True)
        
        if submitted:
            # Validate input
            errors = validate_profile_data(name, age, weight, height, goal_weight)
            
            if errors:
                for error in errors:
                    st.error(f"❌ {error}")
            else:
                # Calculate metrics
                bmi = calculate_bmi(weight, height)
                bmr = calculate_bmr(weight, height, age, gender)
                tdee = calculate_tdee(bmr, activity_level)
                
                # Save profile
                profile_data = {
                    'user_id': 'default_user',
                    'name': name,
                    'age': age,
                    'gender': gender,
                    'height': height,
                    'weight': weight,
                    'goal_weight': goal_weight,
                    'goal': goal,
                    'experience': experience,
                    'activity_level': activity_level,
                    'diet_preference': diet_preference,
                    'bmi': bmi,
                    'bmr': bmr,
                    'tdee': tdee
                }
                
                save_user_profile(profile_data)
                st.session_state.user_profile = profile_data
                st.success("✅ Profile saved successfully!")
                st.balloons()
    
    # Display stats
    if st.session_state.user_profile:
        st.markdown("---")
        st.subheader("📊 Your Stats")
        
        col1, col2, col3, col4 = st.columns(4)
        
        profile = st.session_state.user_profile
        bmi = profile.get('bmi', 0)
        bmi_category, bmi_icon = get_bmi_category(bmi)
        
        with col1:
            st.metric("BMI", f"{bmi:.1f}", f"{bmi_icon} {bmi_category}")
        with col2:
            st.metric("BMR", f"{profile.get('bmr', 0):.0f} cal/day")
        with col3:
            st.metric("TDEE", f"{profile.get('tdee', 0):.0f} cal/day")
        with col4:
            weight_diff = abs(profile.get('weight', 0) - profile.get('goal_weight', 0))
            st.metric("To Goal", f"{weight_diff:.1f} kg")


def render_bodyfat_tab():
    """Render the body fat calculator tab."""
    st.markdown("## 📊 Body Fat Calculator")
    st.markdown("Calculate your body fat percentage using advanced measurements")
    
    # Initialize predictor
    if 'bf_predictor' not in st.session_state:
        st.session_state.bf_predictor = BodyFatPredictor()
    
    user_profile = st.session_state.get('user_profile')
    
    with st.form("bodyfat_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Basic Info**")
            age = st.number_input("Age", 15, 100, int(user_profile.get('age', 25)) if user_profile else 25)
            gender = st.selectbox("Gender", ["Male", "Female"],
                                 index=0 if not user_profile else 
                                 (0 if user_profile.get('gender', 'Male') == 'Male' else 1))
            weight = st.number_input("Weight (kg)", 30.0, 200.0,
                                    float(user_profile.get('weight', 70.0)) if user_profile else 70.0, 0.1)
            height = st.number_input("Height (cm)", 100, 250,
                                    int(user_profile.get('height', 170)) if user_profile else 170)
        
        with col2:
            st.markdown("**Circumference Measurements (cm)**")
            st.caption("Use a measuring tape around the widest part")
            neck = st.number_input("Neck", 20.0, 60.0, 37.0, 0.1)
            chest = st.number_input("Chest", 60.0, 150.0, 95.0, 0.1)
            abdomen = st.number_input("Abdomen (Waist)", 50.0, 150.0, 85.0, 0.1)
            hip = st.number_input("Hip", 60.0, 150.0, 95.0, 0.1)
        
        with st.expander("➕ Additional Measurements (Optional)"):
            col3, col4 = st.columns(2)
            with col3:
                thigh = st.number_input("Thigh", 30.0, 100.0, 55.0, 0.1)
                knee = st.number_input("Knee", 20.0, 60.0, 35.0, 0.1)
                ankle = st.number_input("Ankle", 15.0, 40.0, 22.0, 0.1)
            with col4:
                biceps = st.number_input("Biceps", 20.0, 60.0, 30.0, 0.1)
                forearm = st.number_input("Forearm", 15.0, 50.0, 26.0, 0.1)
                wrist = st.number_input("Wrist", 10.0, 30.0, 16.0, 0.1)
        
        calculate_btn = st.form_submit_button("🔬 Calculate Body Fat", use_container_width=True)
        
        if calculate_btn:
            measurements = {
                'age': age, 'gender': gender.lower(), 'weight': weight, 'height': height,
                'neck': neck, 'chest': chest, 'abdomen': abdomen, 'hip': hip,
                'thigh': thigh, 'knee': knee, 'ankle': ankle,
                'biceps': biceps, 'forearm': forearm, 'wrist': wrist
            }
            
            body_fat = st.session_state.bf_predictor.predict(measurements)
            category, icon = get_body_fat_category(body_fat, gender.lower())
            
            st.session_state.body_fat_result = {
                'percentage': body_fat,
                'category': category,
                'icon': icon,
                'measurements': measurements
            }
    
    # Display results
    if 'body_fat_result' in st.session_state:
        st.markdown("---")
        st.subheader("📈 Your Results")
        
        result = st.session_state.body_fat_result
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Body Fat Percentage", f"{result['percentage']:.1f}%")
        with col2:
            st.metric("Category", f"{result['icon']} {result['category']}")
        with col3:
            weight = result['measurements']['weight']
            lean_mass = weight * (1 - result['percentage'] / 100)
            fat_mass = weight - lean_mass
            st.metric("Lean Mass", f"{lean_mass:.1f} kg")
            st.metric("Fat Mass", f"{fat_mass:.1f} kg")


def render_workout_tab():
    """Render the workout generator tab."""
    st.markdown("## 💪 Workout Generator")
    st.markdown("Generate personalized workout plans tailored to your needs")
    
    # Initialize generator
    if 'workout_gen' not in st.session_state:
        st.session_state.workout_gen = WorkoutGenerator()
    
    user_profile = st.session_state.get('user_profile')
    
    col1, col2 = st.columns(2)
    
    with col1:
        location = st.selectbox("Workout Location", WORKOUT_LOCATIONS)
        workout_type = st.selectbox("Workout Type", WORKOUT_TYPES)
    
    with col2:
        experience_level = st.selectbox("Experience Level", EXPERIENCE_LEVELS,
                                       index=EXPERIENCE_LEVELS.index(user_profile.get('experience', 'Beginner'))
                                       if user_profile and user_profile.get('experience') in EXPERIENCE_LEVELS else 0)
        duration = st.slider("Workout Duration (minutes)", 15, 90, 45, 5)
    
    if st.button("🎲 Generate Workout Plan", use_container_width=True, type="primary"):
        with st.spinner("Generating your personalized workout..."):
            workout_plan = st.session_state.workout_gen.generate_workout(
                location=location,
                workout_type=workout_type,
                experience_level=experience_level,
                duration_minutes=duration
            )
            st.session_state.current_workout = workout_plan
            st.success("✅ Workout plan generated!")
    
    # Display workout
    if 'current_workout' in st.session_state:
        workout = st.session_state.current_workout
        
        st.markdown("---")
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("📍 Location", workout['location'])
        with col2:
            st.metric("🏋️ Type", workout['type'])
        with col3:
            st.metric("📊 Level", workout['level'])
        with col4:
            st.metric("⏱️ Duration", f"{workout['duration']} min")
        
        st.markdown("---")
        st.subheader("🔥 Warmup (5 minutes)")
        
        for exercise in workout['warmup']:
            st.write(f"• **{exercise['name']}** - {exercise['duration']}")
        
        st.markdown("---")
        st.subheader("💪 Main Workout")
        
        for idx, exercise in enumerate(workout['exercises'], 1):
            with st.expander(f"**Exercise {idx}: {exercise['name']}**", expanded=True):
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.markdown(f"**Sets:** {exercise['sets']}")
                with col2:
                    st.markdown(f"**Reps/Duration:** {exercise['reps']}")
                with col3:
                    st.markdown(f"**Rest:** {exercise['rest']}")
        
        st.markdown("---")
        st.subheader("🧘 Cooldown (5-7 minutes)")
        
        for exercise in workout['cooldown']:
            st.write(f"• **{exercise['name']}** - {exercise['duration']}")


def render_meal_tab():
    """Render the meal planner tab."""
    st.markdown("## 🍽️ Meal Planner")
    st.markdown("Generate personalized Indian meal plans based on your goals")
    
    # Initialize planner
    if 'meal_planner' not in st.session_state:
        st.session_state.meal_planner = MealPlanner()
    
    user_profile = st.session_state.get('user_profile')
    
    col1, col2 = st.columns(2)
    
    with col1:
        diet_preference = st.selectbox("Diet Preference", DIET_PREFERENCES,
                                      index=DIET_PREFERENCES.index(user_profile.get('diet_preference', 'Vegetarian'))
                                      if user_profile and user_profile.get('diet_preference') in DIET_PREFERENCES else 0)
        goal = st.selectbox("Goal", ["Weight Loss", "Muscle Gain", "Maintenance"],
                           index=0 if not user_profile else 
                           (["Weight Loss", "Muscle Gain", "Maintenance"].index(user_profile.get('goal', 'Weight Loss'))
                            if user_profile.get('goal') in ["Weight Loss", "Muscle Gain", "Maintenance"] else 0))
    
    with col2:
        default_calories = user_profile.get('tdee', 2000) if user_profile else 2000
        calorie_target = st.number_input("Daily Calorie Target (TDEE)", 1200, 4000, 
                                        int(default_calories), 50)
        num_days = st.slider("Number of Days", 1, 7, 7)
    
    if st.button("🎲 Generate Meal Plan", use_container_width=True, type="primary"):
        with st.spinner("Generating your personalized meal plan..."):
            meal_plan = st.session_state.meal_planner.generate_meal_plan(
                diet_preference=diet_preference,
                calorie_target=calorie_target,
                num_days=num_days,
                goal=goal
            )
            st.session_state.current_meal_plan = meal_plan
            st.success("✅ Meal plan generated!")
    
    # Display meal plan
    if 'current_meal_plan' in st.session_state:
        meal_plan = st.session_state.current_meal_plan
        
        st.markdown("---")
        
        day_options = [f"Day {day['day']}" for day in meal_plan]
        selected_day = st.selectbox("Select Day", day_options)
        day_index = int(selected_day.split()[1]) - 1
        day_plan = meal_plan[day_index]
        
        st.subheader(f"📅 {selected_day} Summary")
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("🔥 Calories", f"{day_plan['total_calories']:.0f}")
        with col2:
            st.metric("🥩 Protein", f"{day_plan['total_protein']:.0f}g")
        with col3:
            st.metric("🍚 Carbs", f"{day_plan['total_carbs']:.0f}g")
        with col4:
            st.metric("🥑 Fat", f"{day_plan['total_fat']:.0f}g")
        
        st.markdown("---")
        st.subheader("🍽️ Meals")
        
        icons = {'Breakfast': '🌅', 'Lunch': '☀️', 'Dinner': '🌙', 'Snacks': '🍎'}
        
        for meal in day_plan['meals']:
            meal_type = meal['type']
            food = meal['food']
            
            with st.expander(f"{icons.get(meal_type, '🍽️')} **{meal_type}: {food['name']}**", expanded=True):
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.markdown(f"**Calories:** {food['calories']}")
                with col2:
                    st.markdown(f"**Protein:** {food['protein']}g")
                with col3:
                    st.markdown(f"**Carbs:** {food['carbs']}g")
                with col4:
                    st.markdown(f"**Fat:** {food['fat']}g")


def render_ai_coach_tab():
    """Render the AI chat coach tab."""
    st.markdown("## 🤖 AI Chat Coach")
    st.markdown("Chat with your personal AI fitness coach for guidance and motivation")
    
    # Initialize coach
    if 'ai_coach' not in st.session_state:
        st.session_state.ai_coach = AICoach()
    
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
    
    # Check API key
    if not GEMINI_API_KEY:
        st.warning("""
        ⚠️ **AI Coach Not Configured**
        
        To use the AI Chat Coach:
        1. Get a free API key from [Google AI Studio](https://makersuite.google.com/app/apikey)
        2. Create a `.env` file in the project root
        3. Add: `GEMINI_API_KEY=your_api_key_here`
        4. Restart the application
        """)
        return
    
    # Display chat history
    if not st.session_state.chat_history:
        st.info("👋 Hi! I'm your AI Fitness Coach. Ask me anything about fitness, nutrition, or workouts!")
    else:
        for message in st.session_state.chat_history:
            if message['role'] == 'user':
                st.markdown(f"""
                <div style="background: #e3f2fd; padding: 1rem; border-radius: 10px; margin: 0.5rem 0;">
                    <b>You:</b> {message['content']}
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div style="background: #f3e5f5; padding: 1rem; border-radius: 10px; margin: 0.5rem 0;">
                    <b>🤖 AI Coach:</b> {message['content']}
                </div>
                """, unsafe_allow_html=True)
    
    # Chat input
    user_input = st.chat_input("Ask your fitness coach anything...")
    
    if user_input:
        st.session_state.chat_history.append({'role': 'user', 'content': user_input})
        
        user_context = st.session_state.get('user_profile')
        
        with st.spinner("🤖 Coach is thinking..."):
            response = st.session_state.ai_coach.get_response(user_input, user_context)
        
        st.session_state.chat_history.append({'role': 'assistant', 'content': response})
        st.rerun()


def render_progress_tab():
    """Render the progress tracker tab."""
    st.markdown("## 📈 Progress Tracker")
    st.markdown("Track your fitness journey and visualize your transformation")
    
    user_profile = st.session_state.get('user_profile')
    
    if not user_profile:
        st.warning("⚠️ Please create your profile first in the User Profile tab!")
        return
    
    user_id = st.session_state.get('user_id', 'default_user')
    progress_history = load_progress_history(user_id)
    
    st.subheader("➕ Log Progress")
    
    with st.form("progress_form"):
        col1, col2, col3 = st.columns(3)
        
        with col1:
            entry_date = st.date_input("Date", value=datetime.now())
            current_weight = st.number_input("Current Weight (kg)", 30.0, 200.0,
                                            float(user_profile.get('weight', 70.0)), 0.1)
        
        with col2:
            body_fat = st.number_input("Body Fat % (optional)", 5.0, 50.0, 20.0, 0.1)
            waist = st.number_input("Waist (cm, optional)", 50.0, 150.0, 85.0, 0.1)
        
        with col3:
            chest = st.number_input("Chest (cm, optional)", 60.0, 150.0, 95.0, 0.1)
            arms = st.number_input("Arms (cm, optional)", 20.0, 60.0, 30.0, 0.1)
        
        notes = st.text_area("Notes", placeholder="How are you feeling? Any achievements?")
        
        submitted = st.form_submit_button("💾 Save Progress", use_container_width=True)
        
        if submitted:
            progress_data = {
                'date': entry_date.isoformat(),
                'weight': current_weight,
                'body_fat': body_fat,
                'waist': waist,
                'chest': chest,
                'arms': arms,
                'notes': notes
            }
            
            save_progress_entry(user_id, progress_data)
            st.success("✅ Progress saved!")
            st.balloons()
            progress_history = load_progress_history(user_id)
    
    # Display progress
    if progress_history:
        st.markdown("---")
        st.subheader("📊 Your Progress")
        
        df = pd.DataFrame(progress_history)
        df['date'] = pd.to_datetime(df['date'])
        df = df.sort_values('date')
        
        start_weight = df['weight'].iloc[0]
        current_weight = df['weight'].iloc[-1]
        goal_weight = user_profile.get('goal_weight', start_weight)
        
        weight_change = start_weight - current_weight
        weight_to_goal = abs(current_weight - goal_weight)
        
        if goal_weight < start_weight:
            progress_percentage = (weight_change / (start_weight - goal_weight)) * 100
        else:
            progress_percentage = (abs(weight_change) / (goal_weight - start_weight)) * 100
        
        progress_percentage = max(0, min(100, progress_percentage))
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Starting Weight", f"{start_weight:.1f} kg")
        with col2:
            st.metric("Current Weight", f"{current_weight:.1f} kg",
                     delta=f"{-weight_change:.1f} kg" if weight_change > 0 else f"+{abs(weight_change):.1f} kg")
        with col3:
            st.metric("Goal Weight", f"{goal_weight:.1f} kg", delta=f"{weight_to_goal:.1f} kg to go")
        with col4:
            st.metric("Progress", f"{progress_percentage:.1f}%")
        
        st.progress(progress_percentage / 100)
        
        motivation = get_motivational_message(progress_percentage)
        st.success(motivation)
        
        # Weight chart
        st.markdown("---")
        st.subheader("📉 Weight Progress Chart")
        
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=df['date'], y=df['weight'],
            mode='lines+markers',
            name='Actual Weight',
            line=dict(color='#667eea', width=3),
            marker=dict(size=8)
        ))
        
        fig.add_trace(go.Scatter(
            x=[df['date'].iloc[0], df['date'].iloc[-1]],
            y=[goal_weight, goal_weight],
            mode='lines',
            name='Goal Weight',
            line=dict(color='#f5576c', width=2, dash='dash')
        ))
        
        fig.update_layout(
            title="Weight Over Time",
            xaxis_title="Date",
            yaxis_title="Weight (kg)",
            height=400,
            hovermode='x unified'
        )
        
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("📝 No progress entries yet. Start tracking your journey by logging your first entry above!")


# ============================================================================
# MAIN APPLICATION
# ============================================================================

def main():
    """Main application entry point."""
    # Load custom styles
    load_custom_styles()
    
    # Initialize session state
    init_session_state()
    
    # Render header
    render_header()
    
    # Create tabs
    tabs = st.tabs([
        "🏠 Home",
        "👤 Profile",
        "📊 Body Fat",
        "💪 Workout",
        "🍽️ Meals",
        "🤖 AI Coach",
        "📈 Progress"
    ])
    
    with tabs[0]:
        render_home_tab()
    
    with tabs[1]:
        render_profile_tab()
    
    with tabs[2]:
        render_bodyfat_tab()
    
    with tabs[3]:
        render_workout_tab()
    
    with tabs[4]:
        render_meal_tab()
    
    with tabs[5]:
        render_ai_coach_tab()
    
    with tabs[6]:
        render_progress_tab()
    
    # Footer
    st.markdown("---")
    st.markdown("""
        <div style="text-align: center; color: #666; padding: 2rem 0;">
            <p>💪 <b>AI Fitness Assistant</b> - Your journey to a healthier you starts here!</p>
            <p style="font-size: 0.9rem;">Built for GymRats 🏋️ | Powered by AI & Dedication</p>
        </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
