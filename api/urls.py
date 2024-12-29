from django.urls import path
from api.views.VeterinarianView import VeterinarianView
from api.views.AnimalView import AnimalView
from api.views.OwnerView import OwnerView

urlpatterns = [
    path('veterinarian/', VeterinarianView.as_view(), name='veterinarians'),
    path('animal/', AnimalView.as_view(), name='animals'),
    path('animal/<str:animal_id>/', AnimalView.as_view(), name='animal-detail'),
    path('owner/', OwnerView.as_view(), name='owners'),
    path('owner/<str:owner_id>/', OwnerView.as_view(), name='owner-detail'),
]
