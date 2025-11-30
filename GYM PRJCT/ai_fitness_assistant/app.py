import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime
import base64
import os

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

st.set_page_config(
    page_title="AI Fitness Assistant",
    page_icon="💪",
    layout="wide",
    initial_sidebar_state="collapsed"
)


def init_auth_state():
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
    st.session_state.authenticated = False
    st.session_state.user_id = None
    st.session_state.username = None
    st.session_state.user_profile = None
    st.session_state.onboarding_step = 0
    st.rerun()


def load_auth_styles():
    bg_image_path = os.path.join("assets", "bg.png")
    bg_image_css = ""
    
    if os.path.exists(bg_image_path):
        with open(bg_image_path, "rb") as f:
            data = f.read()
            encoded = base64.b64encode(data).decode()
            bg_image_css = f"background-image: linear-gradient(rgba(0, 0, 0, 0.7), rgba(0, 0, 0, 0.85)), url('data:image/png;base64,{encoded}'); background-size: cover; background-position: center; background-repeat: no-repeat; background-attachment: fixed;"
    else:
        bg_image_css = "background: linear-gradient(135deg, #0a0a0a 0%, #1a1a2e 50%, #0f0f0f 100%); background-attachment: fixed;"

    st.markdown(f"""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Oswald:wght@400;500;600;700&family=Roboto:wght@300;400;500;700;900&display=swap');
        
        * {{ 
            font-family: 'Roboto', sans-serif;
        }}
        
        h1, h2, h3 {{ 
            font-family: 'Bebas Neue', sans-serif !important; 
            letter-spacing: 3px;
        }}
        
        .stApp {{
            {bg_image_css}
        }}
        
        .main .block-container {{
            position: relative;
            z-index: 10;
        }}
        
        .gym-entrance {{
            max-width: 1000px;
            margin: 0 auto;
            padding: 2rem 1rem;
        }}
        
        .gym-hero {{
            text-align: center;
            margin-bottom: 3rem;
            animation: fadeInDown 1.2s cubic-bezier(0.4, 0, 0.2, 1);
            perspective: 1000px;
        }}
        
        @keyframes fadeInDown {{
            from {{
                opacity: 0;
                transform: translateY(-80px) rotateX(20deg);
            }}
            to {{
                opacity: 1;
                transform: translateY(0) rotateX(0);
            }}
        }}
        
        .gym-hero h1 {{
            font-size: 6rem;
            font-weight: 900;
            color: #ff6b35;
            text-transform: uppercase;
            margin: 0;
            text-shadow: 
                0 0 10px rgba(255, 107, 53, 0.8),
                0 0 20px rgba(255, 107, 53, 0.6),
                0 0 30px rgba(255, 107, 53, 0.4),
                0 0 40px rgba(255, 107, 53, 0.2),
                0 5px 10px rgba(0, 0, 0, 0.5);
            letter-spacing: 8px;
            animation: neonGlow 2s ease-in-out infinite alternate,
                       float 3s ease-in-out infinite;
            position: relative;
            display: inline-block;
        }}
        
        @keyframes neonGlow {{
            from {{ 
                text-shadow: 
                    0 0 10px rgba(255, 107, 53, 0.8),
                    0 0 20px rgba(255, 107, 53, 0.6),
                    0 0 30px rgba(255, 107, 53, 0.4),
                    0 5px 10px rgba(0, 0, 0, 0.5);
            }}
            to {{ 
                text-shadow: 
                    0 0 20px rgba(255, 107, 53, 1),
                    0 0 30px rgba(255, 107, 53, 0.8),
                    0 0 40px rgba(255, 107, 53, 0.6),
                    0 0 50px rgba(255, 107, 53, 0.4),
                    0 5px 15px rgba(0, 0, 0, 0.7);
            }}
        }}
        
        @keyframes float {{
            0%, 100% {{ transform: translateY(0px); }}
            50% {{ transform: translateY(-10px); }}
        }}
        
        .gym-hero .tagline {{
            font-size: 2rem;
            color: #ffffff;
            font-weight: 300;
            margin-top: 1.5rem;
            letter-spacing: 5px;
            text-transform: uppercase;
            text-shadow: 0 2px 10px rgba(0, 0, 0, 0.5);
            animation: fadeIn 1.5s ease-out 0.3s both;
        }}
        
        .gym-hero .motivation {{
            font-size: 1.3rem;
            color: #ff6b35;
            font-weight: 700;
            margin-top: 1.5rem;
            letter-spacing: 3px;
            text-transform: uppercase;
            animation: fadeIn 1.5s ease-out 0.6s both, pulse 2s ease-in-out 2s infinite;
        }}
        
        @keyframes fadeIn {{
            from {{ opacity: 0; transform: translateY(20px); }}
            to {{ opacity: 1; transform: translateY(0); }}
        }}
        
        .auth-container {{
            background: linear-gradient(135deg, 
                rgba(30, 30, 30, 0.95) 0%, 
                rgba(20, 20, 20, 0.98) 100%);
            backdrop-filter: blur(20px) saturate(180%);
            border: 2px solid transparent;
            background-clip: padding-box;
            border-radius: 24px;
            padding: 3rem 2.5rem;
            box-shadow: 
                0 30px 90px rgba(0, 0, 0, 0.9),
                0 0 0 1px rgba(255, 107, 53, 0.3),
                inset 0 1px 0 rgba(255, 255, 255, 0.1);
            position: relative;
            overflow: hidden;
            animation: slideUp 1s cubic-bezier(0.4, 0, 0.2, 1) 0.3s both;
        }}
        
        @keyframes slideUp {{
            from {{
                opacity: 0;
                transform: translateY(60px) scale(0.95);
            }}
            to {{
                opacity: 1;
                transform: translateY(0) scale(1);
            }}
        }}
        
        .auth-container::before {{
            content: '';
            position: absolute;
            top: -2px;
            left: -2px;
            right: -2px;
            bottom: -2px;
            background: linear-gradient(
                45deg,
                #ff6b35,
                #f7931e,
                #ff6b35,
                #f7931e
            );
            background-size: 400% 400%;
            border-radius: 24px;
            z-index: -1;
            animation: borderGlow 4s ease infinite;
        }}
        
        @keyframes borderGlow {{
            0%, 100% {{ background-position: 0% 50%; }}
            50% {{ background-position: 100% 50%; }}
        }}
        
        .auth-container::after {{
            content: '';
            position: absolute;
            top: -50%;
            left: -50%;
            width: 200%;
            height: 200%;
            background: linear-gradient(
                45deg,
                transparent 30%,
                rgba(255, 255, 255, 0.05) 50%,
                transparent 70%
            );
            transform: rotate(45deg);
            animation: shine 6s ease-in-out infinite;
        }}
        
        @keyframes shine {{
            0% {{ transform: translateX(-100%) translateY(-100%) rotate(45deg); }}
            100% {{ transform: translateX(100%) translateY(100%) rotate(45deg); }}
        }}
        
        .auth-header {{
            text-align: center;
            margin-bottom: 2.5rem;
            position: relative;
            z-index: 1;
        }}
        
        .auth-header h2 {{
            color: #ffffff !important;
            font-size: 3.5rem;
            margin-bottom: 0.5rem;
            text-transform: uppercase;
            letter-spacing: 6px;
            text-shadow: 0 0 20px rgba(255, 107, 53, 0.5);
        }}
        
        .auth-header p {{
            color: #cccccc;
            font-size: 1.2rem;
            font-weight: 300;
            letter-spacing: 2px;
        }}
        
        .stTextInput>div>div>input {{
            background: rgba(255, 255, 255, 0.03) !important;
            border: 2px solid rgba(255, 107, 53, 0.3) !important;
            border-radius: 12px !important;
            padding: 1.2rem 1.5rem !important;
            color: #ffffff !important;
            font-size: 1.05rem !important;
            font-weight: 500 !important;
            transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1) !important;
            box-shadow: inset 0 2px 4px rgba(0, 0, 0, 0.3) !important;
        }}
        
        .stTextInput>div>div>input::placeholder {{
            color: #666 !important;
        }}
        
        .stTextInput>div>div>input:focus {{
            border-color: #ff6b35 !important;
            background: rgba(255, 107, 53, 0.08) !important;
            box-shadow: 
                0 0 0 4px rgba(255, 107, 53, 0.15),
                inset 0 2px 4px rgba(0, 0, 0, 0.3),
                0 0 30px rgba(255, 107, 53, 0.3) !important;
            transform: translateY(-2px) !important;
        }}
        
        .stTextInput label {{
            color: #ff6b35 !important;
            font-weight: 700 !important;
            font-size: 0.95rem !important;
            text-transform: uppercase !important;
            letter-spacing: 2px !important;
            text-shadow: 0 0 10px rgba(255, 107, 53, 0.3);
        }}
        
        .stButton>button {{
            background: linear-gradient(135deg, #ff6b35 0%, #f7931e 100%) !important;
            color: #000000 !important;
            border: none !important;
            border-radius: 14px !important;
            padding: 1.1rem 2.5rem !important;
            font-weight: 900 !important;
            font-size: 1.15rem !important;
            text-transform: uppercase !important;
            letter-spacing: 3px !important;
            width: 100% !important;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
            box-shadow: 
                0 8px 25px rgba(255, 107, 53, 0.5),
                0 4px 10px rgba(0, 0, 0, 0.3),
                inset 0 1px 0 rgba(255, 255, 255, 0.3) !important;
            position: relative !important;
            overflow: hidden !important;
        }}
        
        .stButton>button::before {{
            content: '';
            position: absolute;
            top: 50%;
            left: 50%;
            width: 0;
            height: 0;
            background: rgba(255, 255, 255, 0.4);
            border-radius: 50%;
            transform: translate(-50%, -50%);
            transition: width 0.6s, height 0.6s;
        }}
        
        .stButton>button:hover::before {{
            width: 400px;
            height: 400px;
        }}
        
        .stButton>button:hover {{
            transform: translateY(-4px) scale(1.03) !important;
            box-shadow: 
                0 15px 50px rgba(255, 107, 53, 0.7),
                0 8px 20px rgba(0, 0, 0, 0.4),
                inset 0 1px 0 rgba(255, 255, 255, 0.4) !important;
        }}
        
        .stButton>button:active {{
            transform: translateY(-1px) scale(1.01) !important;
        }}
        
        .motivation-box {{
            background: linear-gradient(135deg, 
                rgba(255, 107, 53, 0.15), 
                rgba(247, 147, 30, 0.15));
            border: 2px solid rgba(255, 107, 53, 0.3);
            border-left: 6px solid #ff6b35;
            padding: 2rem;
            margin: 2.5rem 0;
            border-radius: 16px;
            box-shadow: 
                0 10px 40px rgba(255, 107, 53, 0.2),
                inset 0 1px 0 rgba(255, 255, 255, 0.1);
            animation: pulse 4s ease-in-out infinite;
            position: relative;
            overflow: hidden;
        }}
        
        @keyframes pulse {{
            0%, 100% {{ transform: scale(1); box-shadow: 0 10px 40px rgba(255, 107, 53, 0.2); }}
            50% {{ transform: scale(1.02); box-shadow: 0 15px 50px rgba(255, 107, 53, 0.3); }}
        }}
        
        .motivation-box::before {{
            content: '';
            position: absolute;
            top: 0;
            left: -100%;
            width: 100%;
            height: 100%;
            background: linear-gradient(90deg, 
                transparent, 
                rgba(255, 255, 255, 0.1), 
                transparent);
            animation: slideShine 3s ease-in-out infinite;
        }}
        
        @keyframes slideShine {{
            0% {{ left: -100%; }}
            100% {{ left: 100%; }}
        }}
        
        .motivation-box p {{
            color: #ffffff;
            font-size: 1.4rem;
            font-weight: 700;
            margin: 0;
            text-align: center;
            font-style: italic;
            text-shadow: 0 2px 10px rgba(0, 0, 0, 0.5);
            position: relative;
            z-index: 1;
        }}
        
        #MainMenu {{visibility: hidden;}}
        footer {{visibility: hidden;}}
        header {{visibility: hidden;}}
        </style>
    """, unsafe_allow_html=True)


def render_login_page():
    load_auth_styles()
    
    st.markdown("""
        <div class="gym-entrance">
            <div class="gym-hero">
                <h1>GYM ZONE</h1>
                <div style="height: 3px; width: 200px; margin: 1.5rem auto; 
                            background: linear-gradient(90deg, transparent, #ff6b35, transparent);"></div>
                <p class="tagline">AI-POWERED FITNESS REVOLUTION</p>
                <p class="motivation">TRANSFORM YOUR BODY, ELEVATE YOUR MIND</p>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("""
            <div style="text-align: center; padding: 2rem 1.5rem; 
                        background: linear-gradient(135deg, rgba(255, 107, 53, 0.15), rgba(255, 107, 53, 0.05)); 
                        border-radius: 16px; border: 2px solid rgba(255, 107, 53, 0.3);
                        box-shadow: 0 8px 32px rgba(255, 107, 53, 0.2);
                        transition: all 0.3s ease;
                        cursor: pointer;"
                 onmouseover="this.style.transform='translateY(-5px)'; this.style.boxShadow='0 12px 48px rgba(255, 107, 53, 0.4)';"
                 onmouseout="this.style.transform='translateY(0)'; this.style.boxShadow='0 8px 32px rgba(255, 107, 53, 0.2)';">
                <div style="font-size: 3rem; font-weight: 900; color: #ff6b35; 
                            font-family: 'Bebas Neue', sans-serif; 
                            text-shadow: 0 0 20px rgba(255, 107, 53, 0.5);">24/7</div>
                <div style="height: 2px; width: 40px; margin: 0.75rem auto; 
                            background: #ff6b35;"></div>
                <div style="font-size: 0.85rem; color: #cccccc; font-weight: 600;
                            text-transform: uppercase; letter-spacing: 2px;">AI COACH</div>
                <div style="font-size: 0.75rem; color: #888; margin-top: 0.5rem;">Always Available</div>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
            <div style="text-align: center; padding: 2rem 1.5rem; 
                        background: linear-gradient(135deg, rgba(255, 107, 53, 0.15), rgba(255, 107, 53, 0.05)); 
                        border-radius: 16px; border: 2px solid rgba(255, 107, 53, 0.3);
                        box-shadow: 0 8px 32px rgba(255, 107, 53, 0.2);
                        transition: all 0.3s ease;
                        cursor: pointer;"
                 onmouseover="this.style.transform='translateY(-5px)'; this.style.boxShadow='0 12px 48px rgba(255, 107, 53, 0.4)';"
                 onmouseout="this.style.transform='translateY(0)'; this.style.boxShadow='0 8px 32px rgba(255, 107, 53, 0.2)';">
                <div style="font-size: 3rem; font-weight: 900; color: #ff6b35; 
                            font-family: 'Bebas Neue', sans-serif;
                            text-shadow: 0 0 20px rgba(255, 107, 53, 0.5);">100%</div>
                <div style="height: 2px; width: 40px; margin: 0.75rem auto; 
                            background: #ff6b35;"></div>
                <div style="font-size: 0.85rem; color: #cccccc; font-weight: 600;
                            text-transform: uppercase; letter-spacing: 2px;">PERSONALIZED</div>
                <div style="font-size: 0.75rem; color: #888; margin-top: 0.5rem;">Custom Plans</div>
            </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
            <div style="text-align: center; padding: 2rem 1.5rem; 
                        background: linear-gradient(135deg, rgba(255, 107, 53, 0.15), rgba(255, 107, 53, 0.05)); 
                        border-radius: 16px; border: 2px solid rgba(255, 107, 53, 0.3);
                        box-shadow: 0 8px 32px rgba(255, 107, 53, 0.2);
                        transition: all 0.3s ease;
                        cursor: pointer;"
                 onmouseover="this.style.transform='translateY(-5px)'; this.style.boxShadow='0 12px 48px rgba(255, 107, 53, 0.4)';"
                 onmouseout="this.style.transform='translateY(0)'; this.style.boxShadow='0 8px 32px rgba(255, 107, 53, 0.2)';">
                <div style="font-size: 3rem; font-weight: 900; color: #ff6b35; 
                            font-family: 'Bebas Neue', sans-serif;
                            text-shadow: 0 0 20px rgba(255, 107, 53, 0.5);">∞</div>
                <div style="height: 2px; width: 40px; margin: 0.75rem auto; 
                            background: #ff6b35;"></div>
                <div style="font-size: 0.85rem; color: #cccccc; font-weight: 600;
                            text-transform: uppercase; letter-spacing: 2px;">MOTIVATION</div>
                <div style="font-size: 0.75rem; color: #888; margin-top: 0.5rem;">Unlimited Support</div>
            </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    st.markdown('<div class="auth-container">', unsafe_allow_html=True)
    st.markdown("""
        <div class="auth-header">
            <h2>ENTER THE ZONE</h2>
            <div style="height: 3px; width: 100px; margin: 1rem auto; 
                        background: linear-gradient(90deg, transparent, #ff6b35, transparent);"></div>
            <p>Your transformation journey begins now</p>
        </div>
    """, unsafe_allow_html=True)
    
    with st.form("login_form"):
        username = st.text_input("USERNAME OR EMAIL", placeholder="Enter your credentials", label_visibility="visible")
        password = st.text_input("PASSWORD", type="password", placeholder="Enter your password", label_visibility="visible")
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        with col1:
            login_btn = st.form_submit_button("LET'S GO", use_container_width=True)
        with col2:
            if st.form_submit_button("JOIN NOW", use_container_width=True):
                st.session_state.show_signup = True
                st.rerun()
        
        if login_btn:
            if username and password:
                success, message, user_data = auth.login_user(username, password)
                
                if success:
                    st.session_state.authenticated = True
                    st.session_state.user_id = user_data['id']
                    st.session_state.username = user_data['username']
                    st.success("✓ " + message + " - Welcome back, champion!")
                    st.rerun()
                else:
                    st.error("✗ " + message)
            else:
                st.error("✗ Please fill in all fields")
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("""
        <div class="motivation-box">
            <p>"THE ONLY BAD WORKOUT IS THE ONE THAT DIDN'T HAPPEN"</p>
        </div>
    """, unsafe_allow_html=True)


def render_signup_page():
    load_auth_styles()
    
    st.markdown("""
        <div class="gym-entrance">
            <div class="gym-hero">
                <h1>JOIN THE REVOLUTION</h1>
                <div style="height: 3px; width: 200px; margin: 1.5rem auto; 
                            background: linear-gradient(90deg, transparent, #ff6b35, transparent);"></div>
                <p class="tagline">START YOUR TRANSFORMATION TODAY</p>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown('<div class="auth-container">', unsafe_allow_html=True)
    st.markdown("""
        <div class="auth-header">
            <h2>CREATE ACCOUNT</h2>
            <div style="height: 3px; width: 100px; margin: 1rem auto; 
                        background: linear-gradient(90deg, transparent, #ff6b35, transparent);"></div>
            <p>Begin your fitness journey</p>
        </div>
    """, unsafe_allow_html=True)
    
    with st.form("signup_form"):
        username = st.text_input("USERNAME", placeholder="Choose a username", label_visibility="visible")
        email = st.text_input("EMAIL", placeholder="Enter your email", label_visibility="visible")
        password = st.text_input("PASSWORD", type="password", placeholder="Create a strong password", label_visibility="visible")
        confirm_password = st.text_input("CONFIRM PASSWORD", type="password", placeholder="Confirm your password", label_visibility="visible")
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        with col1:
            signup_btn = st.form_submit_button("JOIN NOW", use_container_width=True)
        with col2:
            if st.form_submit_button("BACK TO LOGIN", use_container_width=True):
                st.session_state.show_signup = False
                st.rerun()
        
        if signup_btn:
            if username and email and password and confirm_password:
                if password != confirm_password:
                    st.error("✗ Passwords do not match")
                else:
                    success, message, user_data = auth.create_user(username, email, password)
                    
                    if success:
                        st.session_state.authenticated = True
                        st.session_state.user_id = user_data['id']
                        st.session_state.username = user_data['username']
                        st.success("✓ " + message + " - Welcome to the zone!")
                        st.rerun()
                    else:
                        st.error("✗ " + message)
            else:
                st.error("✗ Please fill in all fields")
    
    st.markdown('</div>', unsafe_allow_html=True)


def main():
    init_auth_state()
    
    if not st.session_state.authenticated:
        if st.session_state.show_signup:
            render_signup_page()
        else:
            render_login_page()
    else:
        from app_dashboard_functions import main as render_dashboard
        render_dashboard()


if __name__ == "__main__":
    main()
