from django.http import StreamingHttpResponse
from django.shortcuts import render, get_object_or_404
from django.db.models import Count, Sum, F


from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .services import open_file
import json


from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from .serializers import *


@login_required(login_url='/api-auth/register/')
def products(request):
    '''Вывод списка продуктов у пользователя'''

    products = ProductAccess.objects.filter(user=request.user).select_related('product')
    return render(request, 'app/products.html', {'products': products})


@login_required(login_url='/api-auth/register/')
def product(request, pk):
    '''Вывод списка уроков продукта'''

    lessons = Lesson.objects.filter(products__id=pk)
    print(lessons)
    return render(request, 'app/product.html', {'lessons': lessons})



@login_required(login_url='/api-auth/register/')
def lesson(request, pk):
    '''Урок'''

    _lesson = get_object_or_404(Lesson, id=pk)
    return render(request, 'app/lesson.html', {'lesson': _lesson})



def update_position(request):
    '''Отслеживат посмотрел ли пользователь ролик'''

    if request.method == 'POST':
        data = json.loads(request.body)

        position = int(data['position'])
        lesson_id = int(data['lesson_id'])

        lesson = Lesson.objects.get(pk=lesson_id)
        duration_seconds = lesson.duration_seconds

        user = request.user
        lesson_view, _ = LessonView.objects.get_or_create(user=user, lesson=lesson)
        lesson_view.current_position_sec = position

        if (position / duration_seconds) >= 0.8:
            # Устанавливаем поле viewed в True
            lesson_view.is_viewed = True

        lesson_view.save()

        return JsonResponse({'message': "You've watched the video!"})
    else:
        return JsonResponse({'message': 'Invalid request method.'})


class LessonListAPIView(generics.ListAPIView):
    '''Список всех уроков по продуктам'''

    serializer_class = ProductAccessSerializer

    def get_queryset(self):
        user = self.request.user
        product_accesses = ProductAccess.objects.filter(user=user)
        return product_accesses


class ProductDetailAPIView(generics.RetrieveAPIView):
    '''Список уроков по конкретному продукту.'''
    def get_queryset(self):
        user = self.request.user
        product_id = self.kwargs['pk']

        if ProductAccess.objects.filter(user=user, product__id=product_id).exists():
            return Product.objects.filter(id=product_id)
        else:
            return Product.objects.none()

    serializer_class = ProductDetailSerializer



class ProductStatsAPIView(generics.ListAPIView):
    '''Статистика по продуктам'''

    serializer_class = ProductStatsSerializer

    def get_queryset(self):
        total_users_count = float(User.objects.count())

        return Product.objects.annotate(
            viewed_lessons_count=Count('lessons__lesson'),
            total_viewing_time=Sum('lessons__lesson__current_position_sec'),
            total_users_product=Count('accesses__user', distinct=True),
            acquisition_percentage=(F('total_users_product') / total_users_count) * 100
        ).values(
            'id', 'name', 'viewed_lessons_count', 'total_viewing_time', 'total_users_product', 'acquisition_percentage',
        )

class UserRegistrationAPIView(generics.CreateAPIView):
    '''Регистрация'''

    serializer_class = UserRegistrationSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response({'message': 'User registered successfully'}, status=status.HTTP_201_CREATED, headers=headers)


def get_streaming_lesson(request, pk: int):
    '''Перемотка урока'''

    file, status_code, content_length, content_range = open_file(request, pk)
    response = StreamingHttpResponse(file, status=status_code, content_type='video/mp4')

    response['Accept-Ranges'] = 'bytes'
    response['Content-Length'] = str(content_length)
    response['Cache-Control'] = 'no-cache'
    response['Content-Range'] = content_range
    return response