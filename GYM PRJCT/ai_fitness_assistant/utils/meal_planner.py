"""
Meal plan generation system with Indian food database
"""
import random
from datetime import datetime

class MealPlanner:
    """Generate personalized meal plans with Indian cuisine"""
    
    def __init__(self):
        self.food_db = self._initialize_food_database()
    
    def _initialize_food_database(self):
        """Initialize Indian food database with nutritional info"""
        return {
            'breakfast': {
                'vegetarian': [
                    {'name': 'Poha', 'calories': 250, 'protein': 6, 'carbs': 45, 'fat': 5},
                    {'name': 'Upma', 'calories': 220, 'protein': 5, 'carbs': 40, 'fat': 4},
                    {'name': 'Idli (3) with Sambar', 'calories': 180, 'protein': 8, 'carbs': 35, 'fat': 2},
                    {'name': 'Dosa with Chutney', 'calories': 200, 'protein': 6, 'carbs': 38, 'fat': 3},
                    {'name': 'Paratha (2) with Curd', 'calories': 320, 'protein': 10, 'carbs': 45, 'fat': 12},
                    {'name': 'Oats Porridge', 'calories': 180, 'protein': 7, 'carbs': 30, 'fat': 4},
                    {'name': 'Vegetable Sandwich', 'calories': 240, 'protein': 8, 'carbs': 35, 'fat': 8},
                ],
                'non-vegetarian': [
                    {'name': 'Egg Bhurji with Roti (2)', 'calories': 280, 'protein': 18, 'carbs': 30, 'fat': 10},
                    {'name': 'Omelette (3 eggs) with Toast', 'calories': 320, 'protein': 22, 'carbs': 25, 'fat': 15},
                    {'name': 'Chicken Sandwich', 'calories': 300, 'protein': 25, 'carbs': 30, 'fat': 10},
                ],
                'eggetarian': [
                    {'name': 'Boiled Eggs (2) with Toast', 'calories': 220, 'protein': 16, 'carbs': 25, 'fat': 8},
                    {'name': 'Egg Dosa', 'calories': 250, 'protein': 14, 'carbs': 30, 'fat': 8},
                ]
            },
            'lunch': {
                'vegetarian': [
                    {'name': 'Dal Rice with Sabzi', 'calories': 400, 'protein': 15, 'carbs': 70, 'fat': 8},
                    {'name': 'Rajma Chawal', 'calories': 450, 'protein': 18, 'carbs': 75, 'fat': 10},
                    {'name': 'Chole Bhature', 'calories': 550, 'protein': 16, 'carbs': 85, 'fat': 18},
                    {'name': 'Paneer Butter Masala with Roti (3)', 'calories': 480, 'protein': 20, 'carbs': 55, 'fat': 20},
                    {'name': 'Veg Biryani', 'calories': 420, 'protein': 12, 'carbs': 70, 'fat': 12},
                    {'name': 'Sambar Rice with Papad', 'calories': 380, 'protein': 12, 'carbs': 68, 'fat': 8},
                    {'name': 'Palak Paneer with Roti (3)', 'calories': 450, 'protein': 22, 'carbs': 50, 'fat': 18},
                ],
                'non-vegetarian': [
                    {'name': 'Chicken Curry with Rice', 'calories': 520, 'protein': 35, 'carbs': 60, 'fat': 15},
                    {'name': 'Fish Curry with Rice', 'calories': 480, 'protein': 32, 'carbs': 58, 'fat': 12},
                    {'name': 'Chicken Biryani', 'calories': 580, 'protein': 30, 'carbs': 70, 'fat': 18},
                    {'name': 'Mutton Curry with Roti (3)', 'calories': 620, 'protein': 38, 'carbs': 50, 'fat': 28},
                    {'name': 'Egg Curry with Rice', 'calories': 450, 'protein': 20, 'carbs': 62, 'fat': 14},
                ],
                'vegan': [
                    {'name': 'Chana Masala with Rice', 'calories': 420, 'protein': 16, 'carbs': 72, 'fat': 10},
                    {'name': 'Mixed Veg Curry with Roti (3)', 'calories': 380, 'protein': 12, 'carbs': 65, 'fat': 8},
                ]
            },
            'dinner': {
                'vegetarian': [
                    {'name': 'Roti (3) with Dal and Sabzi', 'calories': 380, 'protein': 14, 'carbs': 60, 'fat': 10},
                    {'name': 'Khichdi with Curd', 'calories': 320, 'protein': 12, 'carbs': 55, 'fat': 8},
                    {'name': 'Paneer Tikka with Roti (2)', 'calories': 420, 'protein': 24, 'carbs': 40, 'fat': 18},
                    {'name': 'Vegetable Pulao with Raita', 'calories': 360, 'protein': 10, 'carbs': 62, 'fat': 10},
                    {'name': 'Aloo Gobi with Roti (3)', 'calories': 340, 'protein': 10, 'carbs': 58, 'fat': 8},
                ],
                'non-vegetarian': [
                    {'name': 'Grilled Chicken with Roti (2)', 'calories': 420, 'protein': 38, 'carbs': 35, 'fat': 12},
                    {'name': 'Fish Fry with Salad', 'calories': 350, 'protein': 32, 'carbs': 20, 'fat': 16},
                    {'name': 'Chicken Tandoori with Roti (2)', 'calories': 400, 'protein': 36, 'carbs': 35, 'fat': 10},
                    {'name': 'Egg Curry with Roti (2)', 'calories': 380, 'protein': 18, 'carbs': 42, 'fat': 14},
                ],
                'vegan': [
                    {'name': 'Tofu Curry with Rice', 'calories': 380, 'protein': 18, 'carbs': 58, 'fat': 10},
                    {'name': 'Mixed Dal with Roti (3)', 'calories': 340, 'protein': 16, 'carbs': 60, 'fat': 6},
                ]
            },
            'snacks': {
                'vegetarian': [
                    {'name': 'Fruit Chaat', 'calories': 120, 'protein': 2, 'carbs': 28, 'fat': 1},
                    {'name': 'Roasted Chana', 'calories': 150, 'protein': 8, 'carbs': 25, 'fat': 3},
                    {'name': 'Sprouts Salad', 'calories': 100, 'protein': 7, 'carbs': 18, 'fat': 1},
                    {'name': 'Dhokla (2 pieces)', 'calories': 140, 'protein': 5, 'carbs': 24, 'fat': 3},
                    {'name': 'Masala Chai with Biscuits', 'calories': 160, 'protein': 4, 'carbs': 28, 'fat': 4},
                    {'name': 'Banana with Peanut Butter', 'calories': 200, 'protein': 6, 'carbs': 30, 'fat': 8},
                ],
                'non-vegetarian': [
                    {'name': 'Boiled Eggs (2)', 'calories': 140, 'protein': 12, 'carbs': 2, 'fat': 10},
                    {'name': 'Chicken Tikka (4 pieces)', 'calories': 180, 'protein': 24, 'carbs': 4, 'fat': 8},
                ],
                'vegan': [
                    {'name': 'Mixed Nuts (30g)', 'calories': 180, 'protein': 6, 'carbs': 8, 'fat': 15},
                    {'name': 'Hummus with Veggies', 'calories': 150, 'protein': 6, 'carbs': 18, 'fat': 6},
                ]
            }
        }
    
    def generate_meal_plan(self, diet_preference, calorie_target, num_days=7, goal="maintenance"):
        """Generate a meal plan"""
        diet_pref = diet_preference.lower()
        
        # Adjust calorie target based on goal
        if goal.lower() == "weight loss":
            daily_calories = calorie_target - 500
        elif goal.lower() == "muscle gain":
            daily_calories = calorie_target + 300
        else:
            daily_calories = calorie_target
        
        meal_plan = []
        
        for day in range(1, num_days + 1):
            daily_meals = {
                'day': day,
                'date': datetime.now().strftime("%Y-%m-%d"),
                'total_calories': 0,
                'total_protein': 0,
                'total_carbs': 0,
                'total_fat': 0,
                'meals': []
            }
            
            # Distribute calories: Breakfast 25%, Lunch 35%, Dinner 30%, Snacks 10%
            breakfast_cals = daily_calories * 0.25
            lunch_cals = daily_calories * 0.35
            dinner_cals = daily_calories * 0.30
            snack_cals = daily_calories * 0.10
            
            # Select meals
            breakfast = self._select_meal('breakfast', diet_pref, breakfast_cals)
            lunch = self._select_meal('lunch', diet_pref, lunch_cals)
            dinner = self._select_meal('dinner', diet_pref, dinner_cals)
            snack = self._select_meal('snacks', diet_pref, snack_cals)
            
            for meal_type, meal in [('Breakfast', breakfast), ('Lunch', lunch), 
                                     ('Dinner', dinner), ('Snacks', snack)]:
                if meal:
                    daily_meals['meals'].append({
                        'type': meal_type,
                        'food': meal
                    })
                    daily_meals['total_calories'] += meal['calories']
                    daily_meals['total_protein'] += meal['protein']
                    daily_meals['total_carbs'] += meal['carbs']
                    daily_meals['total_fat'] += meal['fat']
            
            meal_plan.append(daily_meals)
        
        return meal_plan
    
    def _select_meal(self, meal_type, diet_pref, target_calories):
        """Select a meal from the database"""
        # Get available meals for this type and diet preference
        available_meals = []
        
        if diet_pref == 'vegetarian':
            available_meals = self.food_db[meal_type].get('vegetarian', [])
        elif diet_pref == 'non-vegetarian':
            # Include both veg and non-veg options
            available_meals = (self.food_db[meal_type].get('vegetarian', []) + 
                             self.food_db[meal_type].get('non-vegetarian', []))
        elif diet_pref == 'vegan':
            available_meals = self.food_db[meal_type].get('vegan', [])
            if not available_meals:
                available_meals = self.food_db[meal_type].get('vegetarian', [])
        elif diet_pref == 'eggetarian':
            available_meals = (self.food_db[meal_type].get('vegetarian', []) + 
                             self.food_db[meal_type].get('eggetarian', []))
        
        if not available_meals:
            return None
        
        # Find meal closest to target calories
        best_meal = min(available_meals, 
                       key=lambda x: abs(x['calories'] - target_calories))
        
        return best_meal
