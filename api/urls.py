from django.urls import path
from api.views.VeterinarianView import VeterinarianView

urlpatterns = [
    path('veterinarian/', VeterinarianView.as_view(), name='veterinarians'),
]