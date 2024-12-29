from django.urls import path
from api.views.VeterinarianView import VeterinarianView
from api.views.AnimalView import AnimalView

urlpatterns = [
    path('veterinarian/', VeterinarianView.as_view(), name='veterinarians'),
    path('animal/', AnimalView.as_view(), name='animals'),  # For listing and creating animals
    path('animal/<str:animal_id>/', AnimalView.as_view(), name='animal-detail'),  # For retrieving, updating, and deleting a specific animal
]
