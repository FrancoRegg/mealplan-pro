from django.urls import path
from .views import IngredientView

urlpatterns = [
    path('ingredients/', IngredientView.as_view(), name="ingredient")
]
