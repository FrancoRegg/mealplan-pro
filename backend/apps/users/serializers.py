from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    password_confirm = serializers.CharField(write_only= True)

    class Meta:
        model = User
        fields = ['email', 'password', 'password_confirm']
        extra_kwargs = {
            'password': {'write_only': True},
            'password_confirm': {'write_only': True}
            }
        
    def validate(self, data):
        if data['password'] != data['password_confirm']:
            raise serializers.ValidationError("Las contraseñas no coinciden")
        return data

    def create(self, validated_data):
        validated_data.pop('password_confirm')
        user = User(
            email = validated_data['email'],
        )

        user.set_password(validated_data['password'])
        user.save()

        return user