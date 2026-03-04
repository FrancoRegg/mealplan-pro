from django.db import models
from apps.users.models import User
from apps.ingredients.models import Ingredient
from django.core.validators import MinValueValidator, MaxValueValidator

class Menu(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class MenuDay(models.Model):
    class Meta:
        unique_together = ('menu', 'day_number')

    menu = models.ForeignKey(Menu, on_delete=models.CASCADE)
    day_number = models.IntegerField(validators=[
            MinValueValidator(1),
            MaxValueValidator(14)
        ])
    date = models.DateField()
    is_locked = models.BooleanField(default=False)

class Meal(models.Model):
    MEAL_TYPE_CHOICES = [
        ('lunch', 'Lunch'),
        ('dinner', 'Dinner')
    ]

    menu_day = models.ForeignKey(MenuDay, on_delete=models.CASCADE)
    meal_type = models.CharField(max_length=10, choices=MEAL_TYPE_CHOICES)
    total_calories = models.DecimalField(max_digits=7, decimal_places=2, null=True)
    total_protein = models.DecimalField(max_digits=6, decimal_places=2, null=True)
    total_carbs = models.DecimalField(max_digits=6, decimal_places=2, null=True)
    total_fat = models.DecimalField(max_digits=6, decimal_places=2, null=True)

class MealItem(models.Model):
    meal = models.ForeignKey(Meal, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    quantity_grams = models.DecimalField(max_digits=6, decimal_places=2)
    calories = models.DecimalField(max_digits=6, decimal_places=2)
    protein = models.DecimalField(max_digits=5, decimal_places=2)
    carbs = models.DecimalField(max_digits=5, decimal_places=2)
    fat = models.DecimalField(max_digits=5, decimal_places=2)