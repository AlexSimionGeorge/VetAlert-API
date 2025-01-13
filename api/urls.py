from django.urls import path
from api.views.VeterinarianView import VeterinarianView
from api.views.AnimalView import AnimalView
from api.views.OwnerView import OwnerView
from api.views.ItemView import ItemView
from api.views.TreatmentLogView import TreatmentLogView

urlpatterns = [
    path('veterinarian/', VeterinarianView.as_view(), name='veterinarians'),
    path('animal/', AnimalView.as_view(), name='animals'),
    path('animal/<str:animal_id>/', AnimalView.as_view(), name='animal-detail'),
    path('owner/', OwnerView.as_view(), name='owners'),
    path('owner/<str:owner_id>/', OwnerView.as_view(), name='owner-detail'),
    path('item/', ItemView.as_view(), name='items'),
    path('item/<str:item_id>/', ItemView.as_view(), name='item-detail'),
    path('treatmentlog/', TreatmentLogView.as_view(), name='treatment-logs'),
    path('treatmentlog/<str:aid>/', TreatmentLogView.as_view(), name='treatment-log-for-animal'),
]
