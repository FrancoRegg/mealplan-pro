from .models import *
from datetime import date, timedelta
import random

def generate_menu(profile, ingredient_available): #Crea el menu completo en la BD
    today = date.today()
    end_menu = today + timedelta(days=14)

    new_menu = Menu.objects.create( #Objeto menu con usuario 
        user=profile.user,
        name="Menú Generado",
        start_date=today,
        end_date=end_menu,
        is_active=True
    )

    target_calories = float(profile.daily_calories) / 2
    target_protein = float(profile.daily_protein) / 2


    for i in range(7): # Crea pares de dias, 1-2, 3-4...
        start_day = (i * 2) + 1
        end_day = (i * 2) + 2

        # Genera menu de comida y cena para cada par de dias. 
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

        meals_data = {
            'lunch': generate_meal(ingredient_available, target_calories, target_protein),
            'dinner': generate_meal(ingredient_available, target_calories, target_protein) 
        }

        
        # Calculo de totales
        for meal_type, meal_data in meals_data.items():
            total_cal = meal_data['protein_calories'] + meal_data['vegetable_calories'] + meal_data['carbohydrate_calories']
            total_protein = meal_data['protein_protein'] + meal_data['vegetable_protein'] + meal_data['carbohydrate_protein']
            total_carbohydrate = meal_data['protein_carbs'] + meal_data['vegetable_carbs'] + meal_data['carbohydrate_carbs']
            total_fat = meal_data['protein_fat'] + meal_data['vegetable_fat'] + meal_data['carbohydrate_fat']

            # Crea comida para ambos dias (init, final) con los totales calculados
            init_meal = Meal.objects.create( 
                menu_day=initia_day,
                meal_type=meal_type,
                total_calories=total_cal, 
                total_protein=total_protein, 
                total_carbs=total_carbohydrate, 
                total_fat=total_fat
            )

            final_meal = Meal.objects.create(
                menu_day=final_day,
                meal_type=meal_type,
                total_calories=total_cal, 
                total_protein=total_protein, 
                total_carbs=total_carbohydrate, 
                total_fat=total_fat
            )

            items = [
                {
                    'ingredient': meal_data['protein_ingredient'],
                    'quantity_grams': meal_data['protein_g'],
                    'calories': meal_data['protein_calories'],
                    'protein': meal_data['protein_protein'],
                    'carbs': meal_data['protein_carbs'],
                    'fat': meal_data['protein_fat']
                }, 
                {
                    'ingredient': meal_data['vegetable_ingredient'],
                    'quantity_grams': meal_data['vegetable_g'],
                    'calories': meal_data['vegetable_calories'],
                    'protein': meal_data['vegetable_protein'],
                    'carbs': meal_data['vegetable_carbs'],
                    'fat': meal_data['vegetable_fat']
                }, 
                {
                    'ingredient': meal_data['carb_ingredient'],
                    'quantity_grams': meal_data['carbohydrate_g'],
                    'calories': meal_data['carbohydrate_calories'],
                    'protein': meal_data['carbohydrate_protein'],
                    'carbs': meal_data['carbohydrate_carbs'],
                    'fat': meal_data['carbohydrate_fat']
                }
            ]

            # Totales de gramos y macros por comida
            for item in items:
                MealItem.objects.create(meal=init_meal, **item)
                MealItem.objects.create(meal=final_meal, **item)

    return new_menu
 
def generate_meal(available_ingredients, target_calories, target_protein): # Funcion auxiliar, genera una comida individual

    # Filtro por ingredientes disponibles de cada categoria
    proteins = [i for i in available_ingredients if i.category == 'protein']
    carbohydrates = [i for i in available_ingredients if i.category == 'carb']
    vegetables = [i for i in available_ingredients if i.category == 'vegetable']

    # Selecciona un ingrediente aleatorio de cada categoria
    protein_ingredient = random.choice(proteins)
    carb_ingredient = random.choice(carbohydrates)
    vegetable_ingredient = random.choice(vegetables)

    # Calculos de cantidades para proteina, vegetales y carbohidratos
    protein_g = (target_protein * 100) / float(protein_ingredient.protein_100g)
    vegetable_g = 150
    protein_calories = (protein_g * float(protein_ingredient.calories_100g)) / 100
    vegetable_calories = (vegetable_g * float(vegetable_ingredient.calories_100g)) / 100
    remaining_calories = target_calories - protein_calories - vegetable_calories
    remaining_calories = max(remaining_calories, 50.0)
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
        'protein_g':round(protein_g, 2),
        'protein_calories':round(protein_calories, 2),
        'protein_protein':round(protein_protein, 2),
        'protein_carbs':round(protein_carbs, 2),
        'protein_fat':round(protein_fat, 2),
        'vegetable_ingredient':vegetable_ingredient, 
        'vegetable_g':round(vegetable_g, 2), 
        'vegetable_calories':round(vegetable_calories, 2),
        'vegetable_protein':round(vegetable_protein, 2),
        'vegetable_carbs':round(vegetable_carbs, 2),
        'vegetable_fat':round(vegetable_fat, 2),
        'carb_ingredient':carb_ingredient,
        'carbohydrate_g':round(carbohydrate_g, 2),
        'carbohydrate_calories':round(remaining_calories, 2),
        'carbohydrate_protein':round(carbohydrate_protein, 2),
        'carbohydrate_carbs':round(carbohydrate_carbs, 2),
        'carbohydrate_fat':round(carbohydrate_fat, 2)
    }