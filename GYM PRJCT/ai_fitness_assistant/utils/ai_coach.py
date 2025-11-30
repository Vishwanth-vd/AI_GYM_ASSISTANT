"""
AI Chat Coach using Google Gemini
"""
import google.generativeai as genai
from config import GEMINI_API_KEY

class AICoach:
    """AI Fitness Coach using Gemini"""
    
    def __init__(self):
        self.api_key = GEMINI_API_KEY
        self.model = None
        self.chat = None
        self._initialize_model()
    
    def _initialize_model(self):
        """Initialize Gemini model"""
        if self.api_key and self.api_key != "":
            try:
                genai.configure(api_key=self.api_key)
                self.model = genai.GenerativeModel('gemini-1.5-flash')
                self.chat = self.model.start_chat(history=[])
            except Exception as e:
                print(f"Error initializing Gemini: {e}")
                self.model = None
    
    def get_response(self, user_message, user_context=None):
        """Get AI coach response"""
        if not self.model:
            return "⚠️ AI Coach is not configured. Please add your Gemini API key in the .env file."
        
        try:
            # Build context-aware prompt
            system_context = """You are an expert AI Fitness Coach. You provide:
            - Personalized fitness advice
            - Workout tips and form corrections
            - Nutrition guidance (especially Indian cuisine)
            - Motivation and support
            - Evidence-based fitness information
            
            Be friendly, encouraging, and professional. Keep responses concise but helpful.
            """
            
            # Add user context if available
            if user_context:
                context_info = f"\n\nUser Profile:\n"
                context_info += f"- Age: {user_context.get('age', 'N/A')}\n"
                context_info += f"- Gender: {user_context.get('gender', 'N/A')}\n"
                context_info += f"- Goal: {user_context.get('goal', 'N/A')}\n"
                context_info += f"- Experience: {user_context.get('experience', 'N/A')}\n"
                system_context += context_info
            
            # Combine system context with user message
            full_prompt = f"{system_context}\n\nUser: {user_message}\n\nAI Coach:"
            
            # Get response from Gemini
            response = self.chat.send_message(full_prompt)
            return response.text
            
        except Exception as e:
            return f"❌ Error getting response: {str(e)}"
    
    def get_workout_advice(self, exercise_name, user_level="beginner"):
        """Get specific workout advice"""
        prompt = f"Provide form tips and common mistakes for {exercise_name} exercise for a {user_level} level person. Keep it concise."
        return self.get_response(prompt)
    
    def get_nutrition_advice(self, goal, diet_preference):
        """Get nutrition advice"""
        prompt = f"Provide nutrition tips for someone with {goal} goal following a {diet_preference} diet, focusing on Indian cuisine. Keep it concise."
        return self.get_response(prompt)
    
    def analyze_progress(self, progress_data):
        """Analyze user's progress"""
        prompt = f"""Analyze this fitness progress and provide insights:
        Starting Weight: {progress_data.get('start_weight', 'N/A')} kg
        Current Weight: {progress_data.get('current_weight', 'N/A')} kg
        Goal Weight: {progress_data.get('goal_weight', 'N/A')} kg
        Weeks Elapsed: {progress_data.get('weeks', 'N/A')}
        
        Provide brief encouragement and suggestions.
        """
        return self.get_response(prompt)
