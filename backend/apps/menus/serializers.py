from rest_framework import serializers
from .models import *
from apps.ingredients.models import Ingredient

class IngredientMenuSerializer(serializers.ModelSerializer):
    class Meta:
        model=Ingredient
        fields=[
            'id',
            'name'
        ]

class MealItemSerializer(serializers.ModelSerializer):
    ingredient = IngredientMenuSerializer()

    class Meta:
        model=MealItem
        fields=[
            'ingredient',
            'quantity_grams',
            'calories',
            'protein',
            'carbs',
            'fat'
        ]

class MealSerializer(serializers.ModelSerializer):
    items = MealItemSerializer(many=True, source='mealitem_set')

    class Meta:
        model=Meal
        fields=[
            'id', 
            'items',
            'meal_type', 
            'total_calories', 
            'total_protein', 
            'total_carbs', 
            'total_fat'
        ]

class MenuDaySerializer(serializers.ModelSerializer):
    meals = MealSerializer(many=True, source='meal_set')

    class Meta:
        model=MenuDay
        fields=[
            'day_number', 
            'date', 
            'is_locked',
            'meals'
        ]

class MenuSerializer(serializers.ModelSerializer):
    days = MenuDaySerializer(many=True, source='menuday_set')

    class Meta:
        model=Menu
        fields=[
            'id',
            'name',
            'start_date',
            'end_date',
            'is_active',
            'days'
        ]