from django.urls import path
from .views import *

urlpatterns = [
    path('login/', login),
    #path('feed/', get_feed),
    path(r'feed/<int:page>', get_feed),
    path('like/', like),
    path('upload/', upload),
    #path('images/', show_images, name='images'),
    path('<str:rurl>', reg, name='register'),

]
