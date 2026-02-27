def calculate_requirements(sex, height_cm, weight_kg, age, activity_level, goal):
    
    height_cm = float(height_cm)
    weight_kg = float(weight_kg)
    age = float(age)

    formula = (10 * weight_kg) + (6.25 * height_cm) - (5 * age)
    activity_factors = {
        'sedentary': 1.2,
        'light': 1.375,
        'moderate': 1.55,
        'active': 1.725,
        'very_active': 1.9
    }

    if sex == 'male':
        tmb = formula + 5
    else:
        tmb = formula - 161

    factor = activity_factors[activity_level] 
    tdee = tmb * factor

    if goal == 'lose_fat':
        target_adjustment = tdee - 300
    elif goal == 'gain_muscle':
        target_adjustment = tdee + 300
    else:
        target_adjustment = tdee

    daily_protein = 2 * weight_kg
    daily_fat = (target_adjustment * 0.25) / 9
    calories_protein = daily_protein * 4
    calories_fat = daily_fat * 9
    calories_carbs = target_adjustment - calories_protein - calories_fat
    daily_carbs =  calories_carbs / 4

    return {
        'daily_calories':target_adjustment,
        'daily_protein': daily_protein,
        'daily_fat': daily_fat,
        'daily_carbs': daily_carbs
    }