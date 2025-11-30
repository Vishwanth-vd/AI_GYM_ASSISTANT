"""
Workout generation system
"""
import random
from datetime import datetime

class WorkoutGenerator:
    """Generate personalized workout plans"""
    
    def __init__(self):
        self.exercises_db = self._initialize_exercises()
    
    def _initialize_exercises(self):
        """Initialize exercise database"""
        return {
            'home': {
                'strength': {
                    'beginner': [
                        {'name': 'Push-ups', 'sets': 3, 'reps': '8-12', 'rest': '60s'},
                        {'name': 'Bodyweight Squats', 'sets': 3, 'reps': '12-15', 'rest': '60s'},
                        {'name': 'Plank', 'sets': 3, 'reps': '30-45s', 'rest': '45s'},
                        {'name': 'Lunges', 'sets': 3, 'reps': '10 each leg', 'rest': '60s'},
                        {'name': 'Glute Bridges', 'sets': 3, 'reps': '12-15', 'rest': '45s'},
                        {'name': 'Wall Sit', 'sets': 3, 'reps': '30-45s', 'rest': '60s'},
                        {'name': 'Mountain Climbers', 'sets': 3, 'reps': '20', 'rest': '45s'},
                        {'name': 'Tricep Dips (chair)', 'sets': 3, 'reps': '8-12', 'rest': '60s'},
                    ],
                    'intermediate': [
                        {'name': 'Diamond Push-ups', 'sets': 4, 'reps': '10-15', 'rest': '60s'},
                        {'name': 'Jump Squats', 'sets': 4, 'reps': '12-15', 'rest': '60s'},
                        {'name': 'Side Plank', 'sets': 3, 'reps': '45s each', 'rest': '45s'},
                        {'name': 'Bulgarian Split Squats', 'sets': 3, 'reps': '12 each', 'rest': '60s'},
                        {'name': 'Pike Push-ups', 'sets': 3, 'reps': '10-12', 'rest': '60s'},
                        {'name': 'Single Leg Deadlift', 'sets': 3, 'reps': '10 each', 'rest': '60s'},
                        {'name': 'Burpees', 'sets': 4, 'reps': '10-12', 'rest': '60s'},
                    ],
                    'advanced': [
                        {'name': 'One-Arm Push-ups', 'sets': 4, 'reps': '6-8 each', 'rest': '90s'},
                        {'name': 'Pistol Squats', 'sets': 4, 'reps': '8-10 each', 'rest': '90s'},
                        {'name': 'Handstand Push-ups', 'sets': 3, 'reps': '5-8', 'rest': '120s'},
                        {'name': 'Archer Push-ups', 'sets': 4, 'reps': '8-10 each', 'rest': '90s'},
                        {'name': 'Dragon Flags', 'sets': 3, 'reps': '6-8', 'rest': '120s'},
                    ]
                },
                'cardio': {
                    'beginner': [
                        {'name': 'Jumping Jacks', 'sets': 3, 'reps': '30s', 'rest': '30s'},
                        {'name': 'High Knees', 'sets': 3, 'reps': '30s', 'rest': '30s'},
                        {'name': 'Butt Kicks', 'sets': 3, 'reps': '30s', 'rest': '30s'},
                        {'name': 'Step-ups', 'sets': 3, 'reps': '45s', 'rest': '45s'},
                    ],
                    'intermediate': [
                        {'name': 'Burpees', 'sets': 4, 'reps': '45s', 'rest': '30s'},
                        {'name': 'Mountain Climbers', 'sets': 4, 'reps': '45s', 'rest': '30s'},
                        {'name': 'Jump Rope', 'sets': 4, 'reps': '60s', 'rest': '30s'},
                        {'name': 'Box Jumps', 'sets': 3, 'reps': '12-15', 'rest': '60s'},
                    ],
                    'advanced': [
                        {'name': 'Burpee Box Jumps', 'sets': 4, 'reps': '60s', 'rest': '30s'},
                        {'name': 'Sprint Intervals', 'sets': 6, 'reps': '30s sprint', 'rest': '30s'},
                        {'name': 'Plyometric Push-ups', 'sets': 4, 'reps': '10-12', 'rest': '60s'},
                    ]
                }
            },
            'gym': {
                'strength': {
                    'beginner': [
                        {'name': 'Barbell Bench Press', 'sets': 3, 'reps': '8-12', 'rest': '90s'},
                        {'name': 'Lat Pulldown', 'sets': 3, 'reps': '10-12', 'rest': '60s'},
                        {'name': 'Leg Press', 'sets': 3, 'reps': '12-15', 'rest': '90s'},
                        {'name': 'Dumbbell Shoulder Press', 'sets': 3, 'reps': '10-12', 'rest': '60s'},
                        {'name': 'Cable Rows', 'sets': 3, 'reps': '10-12', 'rest': '60s'},
                        {'name': 'Leg Curl', 'sets': 3, 'reps': '12-15', 'rest': '60s'},
                    ],
                    'intermediate': [
                        {'name': 'Barbell Squat', 'sets': 4, 'reps': '8-10', 'rest': '120s'},
                        {'name': 'Deadlift', 'sets': 4, 'reps': '6-8', 'rest': '120s'},
                        {'name': 'Incline Dumbbell Press', 'sets': 4, 'reps': '8-12', 'rest': '90s'},
                        {'name': 'Pull-ups', 'sets': 4, 'reps': '8-12', 'rest': '90s'},
                        {'name': 'Romanian Deadlift', 'sets': 3, 'reps': '10-12', 'rest': '90s'},
                        {'name': 'Barbell Rows', 'sets': 4, 'reps': '8-10', 'rest': '90s'},
                    ],
                    'advanced': [
                        {'name': 'Back Squat (Heavy)', 'sets': 5, 'reps': '5', 'rest': '180s'},
                        {'name': 'Deadlift (Heavy)', 'sets': 5, 'reps': '5', 'rest': '180s'},
                        {'name': 'Weighted Pull-ups', 'sets': 4, 'reps': '6-8', 'rest': '120s'},
                        {'name': 'Front Squat', 'sets': 4, 'reps': '6-8', 'rest': '120s'},
                        {'name': 'Overhead Press', 'sets': 4, 'reps': '6-8', 'rest': '120s'},
                    ]
                },
                'cardio': {
                    'beginner': [
                        {'name': 'Treadmill Walk/Jog', 'sets': 1, 'reps': '20 min', 'rest': '0s'},
                        {'name': 'Stationary Bike', 'sets': 1, 'reps': '15 min', 'rest': '0s'},
                        {'name': 'Elliptical', 'sets': 1, 'reps': '15 min', 'rest': '0s'},
                    ],
                    'intermediate': [
                        {'name': 'Treadmill HIIT', 'sets': 8, 'reps': '1 min sprint/1 min walk', 'rest': '0s'},
                        {'name': 'Rowing Machine', 'sets': 1, 'reps': '20 min', 'rest': '0s'},
                        {'name': 'Stair Climber', 'sets': 1, 'reps': '15 min', 'rest': '0s'},
                    ],
                    'advanced': [
                        {'name': 'Sprint Intervals', 'sets': 10, 'reps': '30s sprint/30s rest', 'rest': '0s'},
                        {'name': 'Assault Bike', 'sets': 1, 'reps': '20 min', 'rest': '0s'},
                        {'name': 'Rowing HIIT', 'sets': 8, 'reps': '500m sprint', 'rest': '60s'},
                    ]
                }
            }
        }
    
    def generate_workout(self, location, workout_type, experience_level, duration_minutes=45):
        """Generate a workout plan"""
        location = location.lower()
        experience_level = experience_level.lower()
        
        # Select appropriate exercises
        if workout_type == "Strength Training":
            exercise_pool = self.exercises_db[location]['strength'][experience_level]
        elif workout_type in ["Cardio", "HIIT"]:
            exercise_pool = self.exercises_db[location]['cardio'][experience_level]
        else:  # Mixed
            strength_pool = self.exercises_db[location]['strength'][experience_level]
            cardio_pool = self.exercises_db[location]['cardio'][experience_level]
            exercise_pool = random.sample(strength_pool, 3) + random.sample(cardio_pool, 2)
        
        # Select exercises based on duration
        num_exercises = min(len(exercise_pool), max(4, duration_minutes // 10))
        selected_exercises = random.sample(exercise_pool, min(num_exercises, len(exercise_pool)))
        
        # Create workout plan
        workout_plan = {
            'date': datetime.now().strftime("%Y-%m-%d"),
            'type': workout_type,
            'location': location.capitalize(),
            'level': experience_level.capitalize(),
            'duration': duration_minutes,
            'warmup': self._get_warmup(),
            'exercises': selected_exercises,
            'cooldown': self._get_cooldown()
        }
        
        return workout_plan
    
    def _get_warmup(self):
        """Get warmup routine"""
        return [
            {'name': 'Arm Circles', 'duration': '30s'},
            {'name': 'Leg Swings', 'duration': '30s each leg'},
            {'name': 'Torso Twists', 'duration': '30s'},
            {'name': 'Light Cardio (Jog in place)', 'duration': '2 min'},
        ]
    
    def _get_cooldown(self):
        """Get cooldown routine"""
        return [
            {'name': 'Walking', 'duration': '3 min'},
            {'name': 'Hamstring Stretch', 'duration': '30s each leg'},
            {'name': 'Quad Stretch', 'duration': '30s each leg'},
            {'name': 'Shoulder Stretch', 'duration': '30s each arm'},
            {'name': 'Deep Breathing', 'duration': '1 min'},
        ]
