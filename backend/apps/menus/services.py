from .models import *
from datetime import date, timedelta
import random

def generate_menu(profile, ingredient_available):
    today = date.today()
    end_menu = today + timedelta(days=14)

    new_menu = Menu.objects.create(
        user=profile.user,
        name="Menú Generado",
        start_date=today,
        end_date=end_menu,
        is_active=True
    )

    target_calories = profile.daily_calories / 2
    target_protein = profile.daily_protein / 2

    for i in range(7):
        start_day = (i * 2) + 1
        end_day = (i * 2) + 2

        initia_day = MenuDay.objects.create(
            menu=new_menu,
            day_number=start_day,
            date=today + timedelta(days=start_day - 1),
            is_locked=False
        )

        final_day = MenuDay.objects.create(
            menu=new_menu,
            day_number=end_day,
            date=today + timedelta(days=end_day - 1),
            is_locked=False
        )

        lunch_data = generate_meal(ingredient_available, target_calories, target_protein)
        dinner_data = generate_meal(ingredient_available, target_calories, target_protein)

        total_cal_lunch = lunch_data['protein_calories'] + lunch_data['vegetable_calories'] + lunch_data['carbohydrate_calories']
        total_fat_lunch = lunch_data['protein_fat'] + lunch_data['vegetable_fat'] + lunch_data['carbohydrate_fat']

        total_cal_dinner = dinner_data['protein_calories'] + dinner_data['vegetable_calories'] + dinner_data['carbohydrate_calories']
        total_fat_dinner = dinner_data['protein_fat'] + dinner_data['vegetable_fat'] + dinner_data['carbohydrate_fat']

        lunch_init = Meal.objects.create(
            menu_day=initia_day,
            meal_type='lunch',
            total_calories=total_cal_lunch, 
            total_protein=lunch_data['protein_g'], 
            total_carbs=lunch_data['carbohydrate_g'], 
            total_fat=total_fat_lunch
        )

        dinner_init = Meal.objects.create(
            menu_day=initia_day,
            meal_type='dinner',
            total_calories=total_cal_dinner, 
            total_protein=dinner_data['protein_g'], 
            total_carbs=dinner_data['carbohydrate_g'], 
            total_fat=total_fat_dinner
        )

        lunch_final = Meal.objects.create(
            menu_day=final_day,
            meal_type='lunch',
            total_calories=total_cal_lunch, 
            total_protein=lunch_data['protein_g'], 
            total_carbs=lunch_data['carbohydrate_g'], 
            total_fat=total_fat_lunch
        )

        dinner_final = Meal.objects.create(
            menu_day=final_day,
            meal_type='dinner',
            total_calories=total_cal_dinner, 
            total_protein=dinner_data['protein_g'], 
            total_carbs=dinner_data['carbohydrate_g'], 
            total_fat=total_fat_dinner
        )

        MealItem.objects.create(
            meal=lunch_init,
            ingredient=lunch_data['protein_ingredient'],
            quantity_grams=lunch_data['protein_g'],
            calories=lunch_data['protein_calories'],
            protein=lunch_data['protein_protein'],
            carbs=lunch_data['protein_carbs'],
            fat=lunch_data['protein_fat']
        )

def generate_meal(available_ingredients, target_calories, target_protein):
    proteins = [i for i in available_ingredients if i.category == 'protein']
    carbohydrates = [i for i in available_ingredients if i.category == 'carb']
    vegetables = [i for i in available_ingredients if i.category == 'vegetable']

    protein_ingredient = random.choice(proteins)
    carb_ingredient = random.choice(carbohydrates)
    vegetable_ingredient = random.choice(vegetables)

    protein_g = (target_protein * 100) / float(protein_ingredient.protein_100g)
    vegetable_g = 150
    protein_calories = (protein_g * float(protein_ingredient.calories_100g)) / 100
    vegetable_calories = (vegetable_g * float(vegetable_ingredient.calories_100g)) / 100
    remaining_calories = target_calories - protein_calories - vegetable_calories
    carbohydrate_g = (remaining_calories * 100) / float(carb_ingredient.calories_100g)

    protein_protein = (protein_g * float(protein_ingredient.protein_100g)) / 100
    protein_carbs = (protein_g * float(protein_ingredient.carbs_100g)) / 100
    protein_fat = (protein_g * float(protein_ingredient.fat_100g)) / 100

    vegetable_protein = (vegetable_g * float(vegetable_ingredient.protein_100g)) / 100
    vegetable_carbs = (vegetable_g * float(vegetable_ingredient.carbs_100g)) / 100
    vegetable_fat = (vegetable_g * float(vegetable_ingredient.fat_100g)) / 100

    carbohydrate_protein = (carbohydrate_g * float(carb_ingredient.protein_100g)) / 100
    carbohydrate_carbs = (carbohydrate_g * float(carb_ingredient.carbs_100g)) / 100
    carbohydrate_fat = (carbohydrate_g * float(carb_ingredient.fat_100g)) / 100

    return {
        'protein_ingredient':protein_ingredient,
        'protein_g':protein_g,
        'protein_calories':protein_calories,
        'protein_protein':protein_protein,
        'protein_carbs':protein_carbs,
        'protein_fat':protein_fat,
        'vegetable_ingredient':vegetable_ingredient,
        'vegetable_g':vegetable_g,
        'vegetable_calories':vegetable_calories,
        'vegetable_protein':vegetable_protein,
        'vegetable_carbs':vegetable_carbs,
        'vegetable_fat':vegetable_fat,
        'carb_ingredient':carb_ingredient,
        'carbohydrate_g':carbohydrate_g,
        'carbohydrate_calories':remaining_calories,
        'carbohydrate_protein':carbohydrate_protein,
        'carbohydrate_carbs':carbohydrate_carbs,
        'carbohydrate_fat':carbohydrate_fat
    }