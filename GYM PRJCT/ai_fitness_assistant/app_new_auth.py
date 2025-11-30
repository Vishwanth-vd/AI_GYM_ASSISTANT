"""
AI Fitness Assistant - With Authentication
Complete fitness tracking application with user authentication and personalized dashboard
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime

# Import modules
from utils.auth import auth
from utils.database import db
from utils.helpers import (
    calculate_bmi, get_bmi_category, calculate_bmr, calculate_tdee,
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

# Page config
st.set_page_config(
    page_title="AI Fitness Assistant",
    page_icon="💪",
    layout="wide",
    initial_sidebar_state="collapsed"
)


# ============================================================================
# AUTHENTICATION STATE MANAGEMENT
# ============================================================================

def init_auth_state():
    """Initialize authentication session state."""
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False
    if 'user_id' not in st.session_state:
        st.session_state.user_id = None
    if 'username' not in st.session_state:
        st.session_state.username = None
    if 'show_signup' not in st.session_state:
        st.session_state.show_signup = False
    if 'onboarding_step' not in st.session_state:
        st.session_state.onboarding_step = 0


def logout():
    """Logout user and clear session."""
    st.session_state.authenticated = False
    st.session_state.user_id = None
    st.session_state.username = None
    st.session_state.user_profile = None
    st.session_state.onboarding_step = 0
    st.rerun()


# ============================================================================
# CSS STYLING
# ============================================================================

def load_auth_styles():
    """Load CSS for authentication pages."""
    st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&family=Montserrat:wght@400;500;600;700;800;900&display=swap');
        
        * { font-family: 'Inter', sans-serif; }
        h1, h2, h3 { font-family: 'Montserrat', sans-serif !important; font-weight: 800 !important; }
        
        .stApp {
            background: linear-gradient(-45deg, #667eea, #764ba2, #f093fb, #4facfe);
            background-size: 400% 400%;
            animation: gradientBG 20s ease infinite;
        }
        
        @keyframes gradientBG {
            0%, 100% { background-position: 0% 50%; }
            50% { background-position: 100% 50%; }
        }
        
        .auth-container {
            max-width: 450px;
            margin: 2rem auto;
            background: rgba(255, 255, 255, 0.98);
            padding: 3rem 2.5rem;
            border-radius: 24px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
        }
        
        .auth-header {
            text-align: center;
            margin-bottom: 2rem;
        }
        
        .auth-header h1 {
            color: #667eea !important;
            font-size: 2.5rem;
            margin-bottom: 0.5rem;
        }
        
        .stButton>button {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            border-radius: 12px;
            padding: 0.85rem 2rem;
            font-weight: 700;
            width: 100%;
            transition: all 0.3s ease;
        }
        
        .stButton>button:hover {
            transform: translateY(-2px);
            box-shadow: 0 8px 25px rgba(102, 126, 234, 0.4);
        }
        
        .stTextInput>div>div>input {
            border-radius: 10px;
            border: 2px solid #e0e0e0;
            padding: 0.75rem 1rem;
        }
        
        .stTextInput>div>div>input:focus {
            border-color: #667eea;
            box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
        }
        </style>
    """, unsafe_allow_html=True)


# ============================================================================
# AUTHENTICATION PAGES
# ============================================================================

def render_login_page():
    """Render login page."""
    load_auth_styles()
    
    st.markdown('<div class="auth-container">', unsafe_allow_html=True)
    st.markdown('<div class="auth-header"><h1>💪 Welcome Back!</h1><p>Login to continue your fitness journey</p></div>', unsafe_allow_html=True)
    
    with st.form("login_form"):
        username = st.text_input("Username or Email", placeholder="Enter your username or email")
        password = st.text_input("Password", type="password", placeholder="Enter your password")
        
        col1, col2 = st.columns(2)
        with col1:
            login_btn = st.form_submit_button("Login", use_container_width=True)
        with col2:
            if st.form_submit_button("Sign Up", use_container_width=True):
                st.session_state.show_signup = True
                st.rerun()
        
        if login_btn:
            if username and password:
                success, message, user_data = auth.login_user(username, password)
                
                if success:
                    st.session_state.authenticated = True
                    st.session_state.user_id = user_data['id']
                    st.session_state.username = user_data['username']
                    st.success(message)
                    st.rerun()
                else:
                    st.error(message)
            else:
                st.error("Please fill in all fields")
    
    st.markdown('</div>', unsafe_allow_html=True)


def render_signup_page():
    """Render signup page."""
    load_auth_styles()
    
    st.markdown('<div class="auth-container">', unsafe_allow_html=True)
    st.markdown('<div class="auth-header"><h1>💪 Join Us!</h1><p>Create your account to get started</p></div>', unsafe_allow_html=True)
    
    with st.form("signup_form"):
        username = st.text_input("Username", placeholder="Choose a username")
        email = st.text_input("Email", placeholder="Enter your email")
        password = st.text_input("Password", type="password", placeholder="Create a password")
        confirm_password = st.text_input("Confirm Password", type="password", placeholder="Confirm your password")
        
        col1, col2 = st.columns(2)
        with col1:
            signup_btn = st.form_submit_button("Create Account", use_container_width=True)
        with col2:
            if st.form_submit_button("Back to Login", use_container_width=True):
                st.session_state.show_signup = False
                st.rerun()
        
        if signup_btn:
            if username and email and password and confirm_password:
                if password != confirm_password:
                    st.error("Passwords do not match")
                else:
                    success, message, user_id = auth.register_user(username, email, password)
                    
                    if success:
                        st.session_state.authenticated = True
                        st.session_state.user_id = user_id
                        st.session_state.username = username
                        st.session_state.onboarding_step = 1
                        st.success(message)
                        st.rerun()
                    else:
                        st.error(message)
            else:
                st.error("Please fill in all fields")
    
    st.markdown('</div>', unsafe_allow_html=True)


# ============================================================================
# ONBOARDING WIZARD
# ============================================================================

def render_onboarding():
    """Render multi-step onboarding wizard."""
    load_auth_styles()
    
    step = st.session_state.onboarding_step
    
    st.markdown(f"""
        <div style="text-align: center; margin: 2rem 0;">
            <h1 style="color: white;">Welcome, {st.session_state.username}! 👋</h1>
            <p style="color: white; font-size: 1.2rem;">Let's set up your profile (Step {step}/3)</p>
        </div>
    """, unsafe_allow_html=True)
    
    # Progress bar
    progress = step / 3
    st.progress(progress)
    
    st.markdown('<div class="auth-container">', unsafe_allow_html=True)
    
    if step == 1:
        render_onboarding_step1()
    elif step == 2:
        render_onboarding_step2()
    elif step == 3:
        render_onboarding_step3()
    
    st.markdown('</div>', unsafe_allow_html=True)


def render_onboarding_step1():
    """Step 1: Personal Information."""
    st.markdown("### 📝 Personal Information")
    
    with st.form("onboarding_step1"):
        name = st.text_input("Full Name", placeholder="Enter your full name")
        
        col1, col2 = st.columns(2)
        with col1:
            age = st.number_input("Age", 15, 100, 25)
            gender = st.selectbox("Gender", ["Male", "Female"])
        with col2:
            height = st.number_input("Height (cm)", 100, 250, 170)
            weight = st.number_input("Weight (kg)", 30.0, 200.0, 70.0, 0.1)
        
        if st.form_submit_button("Next →", use_container_width=True):
            if name:
                st.session_state.onboarding_data = {
                    'name': name, 'age': age, 'gender': gender,
                    'height': height, 'weight': weight
                }
                st.session_state.onboarding_step = 2
                st.rerun()
            else:
                st.error("Please enter your name")


def render_onboarding_step2():
    """Step 2: Fitness Goals."""
    st.markdown("### 🎯 Fitness Goals")
    
    with st.form("onboarding_step2"):
        goal = st.selectbox("Primary Goal", FITNESS_GOALS)
        goal_weight = st.number_input("Target Weight (kg)", 30.0, 200.0, 65.0, 0.1)
        experience = st.selectbox("Experience Level", EXPERIENCE_LEVELS)
        
        col1, col2 = st.columns(2)
        with col1:
            if st.form_submit_button("← Back", use_container_width=True):
                st.session_state.onboarding_step = 1
                st.rerun()
        with col2:
            if st.form_submit_button("Next →", use_container_width=True):
                st.session_state.onboarding_data.update({
                    'goal': goal, 'goal_weight': goal_weight, 'experience': experience
                })
                st.session_state.onboarding_step = 3
                st.rerun()


def render_onboarding_step3():
    """Step 3: Lifestyle & Preferences."""
    st.markdown("### 🏃 Lifestyle & Preferences")
    
    with st.form("onboarding_step3"):
        activity_options = [
            "Sedentary (little or no exercise)",
            "Lightly active (1-3 days/week)",
            "Moderately active (3-5 days/week)",
            "Very active (6-7 days/week)",
            "Super active (athlete)"
        ]
        activity_level = st.select_slider("Activity Level", activity_options, value=activity_options[2])
        diet_preference = st.selectbox("Diet Preference", DIET_PREFERENCES)
        
        col1, col2 = st.columns(2)
        with col1:
            if st.form_submit_button("← Back", use_container_width=True):
                st.session_state.onboarding_step = 2
                st.rerun()
        with col2:
            if st.form_submit_button("Complete Setup ✓", use_container_width=True):
                # Combine all data
                data = st.session_state.onboarding_data
                data.update({'activity_level': activity_level, 'diet_preference': diet_preference})
                
                # Calculate metrics
                data['bmi'] = calculate_bmi(data['weight'], data['height'])
                data['bmr'] = calculate_bmr(data['weight'], data['height'], data['age'], data['gender'])
                data['tdee'] = calculate_tdee(data['bmr'], activity_level)
                data['profile_complete'] = True
                
                # Save to database
                if db.create_profile(st.session_state.user_id, data):
                    st.session_state.onboarding_step = 0
                    st.success("Profile created successfully!")
                    st.balloons()
                    st.rerun()
                else:
                    st.error("Error saving profile. Please try again.")


# ============================================================================
# MAIN APP (After Authentication)
# ============================================================================

# Import the existing app functions from the previous version
# For brevity, I'll include a simplified dashboard here

def render_authenticated_app():
    """Render the main app for authenticated users."""
    # Load profile
    if 'user_profile' not in st.session_state or st.session_state.user_profile is None:
        profile = db.get_profile(st.session_state.user_id)
        if profile:
            st.session_state.user_profile = profile
    
    # Check if profile is complete
    if not st.session_state.get('user_profile') or not st.session_state.user_profile.get('profile_complete'):
        render_onboarding()
        return
    
    # Load the main app styles and render
    from app_no_auth import (
        load_custom_styles, render_header,
        render_home_tab, render_profile_tab, render_bodyfat_tab,
        render_workout_tab, render_meal_tab, render_ai_coach_tab, render_progress_tab
    )
    
    load_custom_styles()
    
    # Header with logout
    col1, col2 = st.columns([6, 1])
    with col1:
        render_header()
    with col2:
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("🚪 Logout"):
            logout()
    
    # Tabs
    tabs = st.tabs([
        "🏠 Home", "👤 Profile", "📊 Body Fat", "💪 Workout",
        "🍽️ Meals", "🤖 AI Coach", "📈 Progress"
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


# ============================================================================
# MAIN APPLICATION ENTRY
# ============================================================================

def main():
    """Main application entry point."""
    init_auth_state()
    
    # Route based on authentication state
    if not st.session_state.authenticated:
        if st.session_state.show_signup:
            render_signup_page()
        else:
            render_login_page()
    else:
        render_authenticated_app()


if __name__ == "__main__":
    main()
