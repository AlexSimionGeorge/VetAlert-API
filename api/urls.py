from django.urls import path
from .views import google_login, VeterinarianView, AnimalView

urlpatterns = [
    path('login/google/', google_login, name='google-login'),
    path('veterinarians/', VeterinarianView.as_view(), name='veterinarians'),
    path('veterinarians/<str:pk>/', VeterinarianView.as_view(), name='veterinarian_detail'),
    path('animals/', AnimalView.as_view(), name='animals'),
    path('animals/<str:pk>/', AnimalView.as_view(), name='animal_detail'),
]