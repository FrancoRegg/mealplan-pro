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