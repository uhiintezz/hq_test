from django.urls import path
from .views import *


urlpatterns = [
    path('stream/<int:pk>/', get_streaming_lesson, name='stream'),
    path('lessons/<int:pk>', lesson, name='lesson'),
    path('lessons/', lessons, name='lessons'),
    path('update_position/', update_position, name='update_position'),


]
