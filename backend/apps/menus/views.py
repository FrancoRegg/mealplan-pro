from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import *
from .serializers import *
from apps.ingredients.models import Ingredient
from apps.profiles.models import Profile
from .services import generate_menu

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