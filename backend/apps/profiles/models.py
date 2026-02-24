from apps.users.models import User
from django.db import models

# Create your models here.
class Profile(models.Model):
    OPTION_SEX_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female')
    ]
    ACTIVITY_LEVEL_CHOICES = [ 
        ('sedentary', 'Sedentary'),
        ('light', 'Light'),
        ('moderate', 'Moderate'),
        ('active', 'Active'),
        ('very_active', 'Very_active')
    ]
    GOAL_CHOICES = [
        ('lose_fat', 'Lose_fat'),
        ('maintain', 'Maintain'),
        ('gain_muscle', 'Gain_muscle')
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    height_cm = models.DecimalField(max_digits=10, decimal_places=2)
    weight_kg = models.DecimalField(max_digits=10, decimal_places=2)
    age = models.IntegerField()
    sex = models.CharField(max_length=10, choices=OPTION_SEX_CHOICES)
    activity_level = models.CharField(max_length=20, choices=ACTIVITY_LEVEL_CHOICES)
    goal = models.CharField(max_length=20, choices=GOAL_CHOICES)
    daily_calories = models.IntegerField(null=True, blank=True)                                 
    daily_protein = models.IntegerField(null=True, blank=True)
    daily_carbs = models.IntegerField(null=True, blank=True)
    daily_fat = models.IntegerField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)