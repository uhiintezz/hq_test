from django.urls import path
from .views import *


urlpatterns = [
    path('stream/<int:pk>/', get_streaming_lesson, name='stream'),
    path('products/', products, name='products'),
    path('product/<int:pk>', product, name='product'),
    path('lesson/<int:pk>', lesson, name='lesson'),
    path('update_position/', update_position, name='update_position'),

    path('api/v1/lesson-views/', LessonListAPIView.as_view(), name='lesson-view-list'), #2.1
    path('api/v1/product/<int:pk>', ProductDetailAPIView.as_view(), name='product-detail'),#2.2
    path('api/v1/product-stats/', ProductStatsAPIView.as_view(), name='product-stats'), #2.3
]
