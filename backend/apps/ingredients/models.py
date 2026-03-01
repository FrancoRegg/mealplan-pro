from django.db import models
from apps.profiles.models import Profile

class Ingredient(models.Model):
    CATEGORY_CHOICES = [
        ('protein', 'Protein'),
        ('carb', 'Carb'),
        ('vegetable', 'Vegetable')
    ]

    name = models.CharField( max_length=100, unique=True, null=False)
    category = models.CharField( max_length=20, choices=CATEGORY_CHOICES)
    calories_100g = models.DecimalField(max_digits=6, decimal_places=2)
    protein_100g = models.DecimalField(max_digits=5, decimal_places=2)
    carbs_100g = models.DecimalField(max_digits=5, decimal_places=2)
    fat_100g = models.DecimalField(max_digits=5, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

class ProfileIngredient(models.Model):
    class Meta:
        unique_together = ('profile', 'ingredient')

    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    is_available = models.BooleanField(default=True)