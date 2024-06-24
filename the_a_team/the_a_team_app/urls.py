from django.urls import path
from .views import get_prediction, generate_new_model, generate_key, home

urlpatterns = [
    path('data/prediction', get_prediction, name='get_prediction'),
    path('data/model', generate_new_model, name='generate_new_model'),
    path('generate_key', generate_key, name='generate_key'),
    path('', home, name="home"),
]
