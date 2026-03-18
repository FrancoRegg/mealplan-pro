from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import *
from .serializers import *
from apps.ingredients.models import Ingredient
from apps.profiles.models import Profile
from .services import *

class GenerateMenuView(APIView):
    def post(self, request):
        try:
            profile = request.user.profile
            available_ingredients = Ingredient.objects.filter(
                profileingredient__profile=profile, 
                profileingredient__is_available=True
            )
            # Verificamos que exista al menos un ingrediente para cada categoria 
            proteins = [i for i in available_ingredients if i.category == 'protein']
            carbohydrates = [i for i in available_ingredients if i.category == 'carb']
            vegetables = [i for i in available_ingredients if i.category == 'vegetable']
            if not proteins or not carbohydrates or not vegetables:
                return Response({'error': 'Debe tener al menos una proteína, un carbohidrato y una verdura disponibles.'}, status=status.HTTP_400_BAD_REQUEST)
            
            # Despues de validar, llamamos a generate_menu() para obtener un menu completo
            menu = generate_menu(profile, available_ingredients)
            serializer_menu = MenuSerializer(menu)
            return Response(serializer_menu.data, status=status.HTTP_201_CREATED)
        except Profile.DoesNotExist:
            return Response({'error': 'Perfil no encontrado. Complete su perfil.'}, status=status.HTTP_404_NOT_FOUND)

class ActiveMenuView(APIView):
    def get(self, request):
        try:
            menu_active = Menu.objects.get(user=request.user, is_active=True)
            serializer_menu_active = MenuSerializer(menu_active)
            return Response(serializer_menu_active.data, status=status.HTTP_200_OK)
        except Menu.DoesNotExist:
            return Response({'error': 'No hay menu activo'}, status=status.HTTP_404_NOT_FOUND)
        
class MenuByIdView(APIView):
    def get(self, request, menu_id):
        try:
            menu = Menu.objects.get(user=request.user, id=menu_id)
            serializer_menu_id = MenuSerializer(menu)
            return Response(serializer_menu_id.data, status=status.HTTP_200_OK)
        except Menu.DoesNotExist:
            return Response({'error': 'El menú no existe'}, status=status.HTTP_404_NOT_FOUND)
        
class RegenerateDayView(APIView):
    def post(self, request, menu_id, day_number):
        try:
            menu = Menu.objects.get(user=request.user, id=menu_id)
            # Obtenemos un dia en particular del menu y verificamos que NO este bloqueado 
            day = MenuDay.objects.get(menu=menu, day_number=day_number)
            if day.is_locked == True:
                return Response({'error': 'El día al que quiere acceder esta bloqueado!'}, status=status.HTTP_400_BAD_REQUEST)
            Meal.objects.filter(menu_day=day).delete() # Se elimina la comida de ese día, mas adelante se crea una nueva

            # Verificamos el perfil del usuario y obtenemos ingredientes disponibles
            profile = request.user.profile
            target_calories = float(profile.daily_calories) / 2
            target_protein = float(profile.daily_protein) / 2
            available_ingredients = Ingredient.objects.filter(
                profileingredient__profile=profile, 
                profileingredient__is_available=True
            )

            # Genera nueva comida y cena   
            meals_data = {
                'lunch': generate_meal(available_ingredients, target_calories, target_protein),
                'dinner': generate_meal(available_ingredients, target_calories, target_protein)
            }

            # Calculos totales
            for meal_type, meal_data in meals_data.items():
                total_cal = meal_data['protein_calories'] + meal_data['vegetable_calories'] + meal_data['carbohydrate_calories']
                total_protein = meal_data['protein_protein'] + meal_data['vegetable_protein'] + meal_data['carbohydrate_protein']
                total_carbohydrate = meal_data['protein_carbs'] + meal_data['vegetable_carbs'] + meal_data['carbohydrate_carbs']
                total_fat = meal_data['protein_fat'] + meal_data['vegetable_fat'] + meal_data['carbohydrate_fat']

                # Crea nueva comida
                meal = Meal.objects.create( 
                    menu_day=day,
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
                
                # Totales de gramos y macros para la comida
                for item in items:
                    MealItem.objects.create(meal=meal, **item)

            serializer_day = MenuDaySerializer(day)
            return Response(serializer_day.data, status=status.HTTP_201_CREATED)    
        except Menu.DoesNotExist:
            return Response({'error': 'Menú no encontrado'}, status=status.HTTP_404_NOT_FOUND)
        except MenuDay.DoesNotExist:
            return Response({'error': 'El día solicitado no existe'}, status=status.HTTP_404_NOT_FOUND)