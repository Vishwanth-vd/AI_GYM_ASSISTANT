# AI Fitness Assistant 💪

A comprehensive AI-powered fitness assistant built with Streamlit that helps you achieve your fitness goals through personalized workout plans, meal planning, body composition tracking, and AI coaching.

## ✨ Features

- **📊 Body Fat Calculator** - Accurate body fat percentage calculation using the Navy Method
- **💪 Workout Generator** - Personalized workout plans for home or gym, adapted to your experience level
- **🍽️ Meal Planner** - Indian cuisine-focused meal plans with complete nutritional tracking
- **🤖 AI Chat Coach** - 24/7 AI-powered fitness coach using Google Gemini
- **📈 Progress Tracker** - Track weight, measurements, and visualize your transformation journey
- **🎯 Goal Prediction** - AI-powered prediction of when you'll reach your fitness goals
- **👤 User Profile** - Complete profile management with BMI, BMR, and TDEE calculations

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- pip package manager

### Installation

1. **Clone or download this project**

2. **Navigate to the project directory**
   ```bash
   cd ai_fitness_assistant
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables (Optional - for AI Coach)**
   
   Create a `.env` file in the project root:
   ```
   GEMINI_API_KEY=your_gemini_api_key_here
   ```
   
   Get your free API key from [Google AI Studio](https://makersuite.google.com/app/apikey)

5. **Run the application**
   ```bash
   streamlit run app.py
   ```

6. **Open your browser**
   
   The app will automatically open at `http://localhost:8501`

## 📖 Usage Guide

### 1. Create Your Profile
- Navigate to **👤 User Profile** from the sidebar
- Fill in your personal information (age, weight, height, goals, etc.)
- Save your profile to unlock personalized features

### 2. Calculate Body Fat
- Go to **📊 Body Fat Calculator**
- Enter your measurements (neck, waist, hip, etc.)
- Get your body fat percentage and body composition breakdown

### 3. Generate Workouts
- Visit **💪 Workout Generator**
- Select your preferences (home/gym, workout type, experience level)
- Generate and save personalized workout plans

### 4. Plan Your Meals
- Open **🍽️ Meal Planner**
- Choose your diet preference and calorie target
- Generate weekly meal plans with Indian cuisine

### 5. Chat with AI Coach
- Go to **🤖 AI Chat Coach**
- Ask questions about fitness, nutrition, or workouts
- Get personalized advice based on your profile

### 6. Track Progress
- Use **📈 Progress Tracker**
- Log your weight and measurements regularly
- Visualize your transformation with charts and graphs

## 🎯 Features in Detail

### Body Fat Calculator
- Uses the Navy Method for accurate body fat estimation
- Provides body composition breakdown (lean mass vs fat mass)
- Categorizes results (Athletes, Fitness, Average, etc.)
- Visual pie charts for easy understanding

### Workout Generator
- **Home workouts** - Bodyweight and minimal equipment exercises
- **Gym workouts** - Full equipment access routines
- **Experience levels** - Beginner, Intermediate, Advanced
- **Workout types** - Strength, Cardio, HIIT, Mixed
- Includes warmup and cooldown routines
- Save and download workout plans

### Meal Planner
- **Indian cuisine focus** - Authentic Indian meals
- **Diet preferences** - Vegetarian, Non-Vegetarian, Vegan, Eggetarian
- **Complete nutrition** - Calories, protein, carbs, fat tracking
- **Weekly plans** - Generate up to 7 days of meals
- **Goal-based** - Adjusted for weight loss, muscle gain, or maintenance
- Visual macronutrient breakdown

### AI Chat Coach
- Powered by Google Gemini AI
- Context-aware responses based on your profile
- Quick action buttons for common questions
- Workout tips, nutrition advice, and motivation
- Chat history for reference

### Progress Tracker
- Log weight and body measurements
- Visual charts showing progress over time
- Goal prediction with estimated target dates
- Motivational messages based on progress
- Weekly trend analysis
- Export progress data

## 🛠️ Technology Stack

- **Frontend & Backend** - Streamlit
- **Data Processing** - Pandas, NumPy
- **Machine Learning** - Scikit-learn
- **Visualizations** - Plotly
- **AI Integration** - Google Gemini API
- **Data Storage** - JSON files

## 📁 Project Structure

```
ai_fitness_assistant/
├── app.py                      # Main application
├── config.py                   # Configuration settings
├── requirements.txt            # Python dependencies
├── .env.example               # Environment variables template
├── utils/
│   ├── helpers.py             # Helper functions
│   ├── ml_models.py           # ML models for predictions
│   ├── workout_generator.py   # Workout generation logic
│   ├── meal_planner.py        # Meal planning system
│   └── ai_coach.py            # AI coach integration
├── pages/
│   ├── 1_👤_User_Profile.py
│   ├── 2_📊_Body_Fat_Calculator.py
│   ├── 3_💪_Workout_Generator.py
│   ├── 4_🍽️_Meal_Planner.py
│   ├── 5_🤖_AI_Chat_Coach.py
│   └── 6_📈_Progress_Tracker.py
├── data/                      # Data storage
├── models/                    # Saved ML models
└── user_data/                 # User profiles and progress
```

## 🔧 Configuration

### Customizing the App

Edit `config.py` to customize:
- App title and icon
- Fitness goals list
- Workout types and locations
- Diet preferences
- UI colors

### Adding Custom Exercises

Edit `utils/workout_generator.py` to add your own exercises to the database.

### Adding Custom Meals

Edit `utils/meal_planner.py` to add more Indian dishes to the food database.

## 📊 Data Storage

All user data is stored locally in JSON format:
- **User profiles** - `user_data/{user_id}_profile.json`
- **Progress entries** - `user_data/{user_id}_progress.json`
- **Workout plans** - `user_data/{user_id}_workout_{date}.json`

## 🤝 Contributing

Contributions are welcome! Feel free to:
- Add more exercises to the workout database
- Expand the Indian food database
- Improve UI/UX
- Add new features
- Fix bugs

## 📝 License

This project is open source and available for personal and educational use.

## 🙏 Acknowledgments

- Google Gemini for AI capabilities
- Streamlit for the amazing framework
- The fitness community for inspiration

## 📧 Support

For issues, questions, or suggestions:
- Create an issue in the repository
- Check the documentation
- Ask the AI Coach within the app!

---

**Made with ❤️ for the fitness community**

Start your fitness journey today! 💪🏃‍♂️🥗
