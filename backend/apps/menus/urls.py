from django.urls import path
from .views import *

urlpatterns = [
    path('generate/', GenerateMenuView.as_view(), name="generate_menu"),
    path('active/', ActiveMenuView.as_view(), name="active_menu"),
    path('<int:menu_id>/', MenuByIdView.as_view(), name="menu_id"),
    path('<int:menu_id>/days/<int:day_number>/regenerate', RegenerateDayView.as_view(), name="regenerate_menu")
]