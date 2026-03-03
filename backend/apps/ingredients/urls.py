from django.urls import path
from .views import *

urlpatterns = [
    path('ingredients/', IngredientView.as_view(), name="ingredient"),
    path('ingredients/availability/', IngredientAvailabilityView.as_view(), name="ingredient_availability"),
    path('ingredients/available/', IngredientAvailableView.as_view(), name="ingredient_available")
]
