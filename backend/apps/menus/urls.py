from django.urls import path
from .views import *

urlpatterns = [
    path('generate/', GenerateMenuView.as_view(), name="generate_menu"),
    path('active/', ActiveMenuView.as_view(), name="active_menu")
]