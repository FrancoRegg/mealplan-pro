from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import *
from apps.profiles.models import Profile
from .serializers import IngredientSerializer

class IngredientView(APIView):
    def get(self, request):
        try:
            serializer = IngredientSerializer(Ingredient.objects.all(), many=True, context={'request': request})
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Profile.DoesNotExist:
            return Response({'error': 'Perfil no encontrado. Complete su perfil.'}, status=status.HTTP_404_NOT_FOUND)

class IngredientAvailableView(APIView):
    def get(self, request):
        try:
            serializer = IngredientSerializer(Ingredient.objects.filter(profileingredient__profile=request.user.profile, profileingredient__is_available=True), many=True, context={'request': request})
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Profile.DoesNotExist:
            return Response({'error': 'Perfil no encontrado. Complete su perfil.'}, status=status.HTTP_404_NOT_FOUND)

class IngredientAvailabilityView(APIView):    
    def put(self, request):
        try:
            ingredients = request.data.get('ingredients')
            for i in ingredients:
                ProfileIngredient.objects.update_or_create(
                    profile=request.user.profile,
                    ingredient=Ingredient.objects.get(id=i['id']),
                    defaults={
                        'is_available':i['is_available']
                    }
                )
            return Response({'message': 'Disponibilidad actualizada correctamente'}, status=status.HTTP_200_OK)
        except Profile.DoesNotExist:
            return Response({'error': 'Perfil no encontrado. Complete su perfil.'}, status=status.HTTP_404_NOT_FOUND)
        except Ingredient.DoesNotExist:
            return Response({'error': 'Ingrediente no encontrado.'}, status=status.HTTP_404_NOT_FOUND)