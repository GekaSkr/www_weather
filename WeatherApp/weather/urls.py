from django.urls import path
from . import views
urlpatterns = [

    path('', views.index),
    path('kharkiv',  views.kharkiv),
    path('kharkiv_7',  views.kharkiv_7),
    path( 'delete', views.Delete, name = 'delete'),

]
