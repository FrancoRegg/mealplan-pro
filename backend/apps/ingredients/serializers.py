from rest_framework import serializers
from .models import *

class IngredientSerializer(serializers.ModelSerializer):
    is_available = serializers.SerializerMethodField()

    class Meta:
        model= Ingredient
        fields= [
            'id',
            'name',
            'category',
            'calories_100g',
            'protein_100g',
            'carbs_100g',
            'fat_100g',
            'is_available'
        ]
    

    def get_is_available(self, obj):
        request = self.context.get('request')
        profile = request.user.profile
        availability = ProfileIngredient.objects.filter(
            ingredient=obj, 
            profile=profile, 
            is_available=True
        )
        return availability.exists()
        