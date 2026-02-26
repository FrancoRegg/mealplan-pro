from rest_framework import serializers
from .services import calculate_requirements
from .models import Profile

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = [
            'height_cm', 
            'weight_kg', 
            'age', 
            'sex', 
            'activity_level', 
            'goal', 
            'daily_calories', 
            'daily_protein', 
            'daily_carbs', 
            'daily_fat'
        ]
        read_only_fields = ['daily_calories', 'daily_protein', 'daily_carbs', 'daily_fat']

    def create(self, validated_data):
        data = calculate_requirements(
            height_cm=validated_data.get('height_cm'),
            weight_kg=validated_data.get('weight_kg'),
            age=validated_data.get('age'),
            sex=validated_data.get('sex'),
            activity_level=validated_data.get('activity_level'),
            goal=validated_data.get('goal'),
        )

        validated_data.update(data)
        profile = Profile.objects.create(**validated_data)
        return profile
        
    def update(self, instance, validated_data):
        instance.height_cm = validated_data.get('height_cm', instance.height_cm)
        instance.weight_kg = validated_data.get('weight_kg', instance.weight_kg)
        instance.age = validated_data.get('age', instance.age)
        instance.sex = validated_data.get('sex', instance.sex)
        instance.activity_level = validated_data.get('activity_level', instance.activity_level)
        instance.goal = validated_data.get('goal', instance.goal)
        
        data = calculate_requirements(
            validated_data.get('height_cm', instance.height_cm),
            validated_data.get('weight_kg', instance.weight_kg),
            validated_data.get('age', instance.age),
            validated_data.get('sex', instance.sex),
            validated_data.get('activity_level', instance.activity_level),
            validated_data.get('goal', instance.goal)
        )
        
        instance.daily_calories = data['daily_calories']
        instance.daily_protein = data['daily_protein']
        instance.daily_carbs = data['daily_carbs']
        instance.daily_fat = data['daily_fat']

        instance.save()
        return instance

