from django.urls import path
from . import views

urlpatterns = [
    path('index/', views.index, name='index'),  # Solve page
    path('results/', views.results, name='results'),  # Results page
    path('about/', views.about, name='about'),  # About page
]