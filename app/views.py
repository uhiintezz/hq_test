from django.http import StreamingHttpResponse
from django.shortcuts import render, get_object_or_404
from .models import *
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .services import open_file
import json

from rest_framework.permissions import IsAuthenticated
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from .serializers import *


@login_required(login_url='/api/auth/register/')
def lessons(request):
    lessons = Lesson.objects.all()
    return render(request, 'app/lessons.html', {'lessons': lessons})


@login_required(login_url='/api/auth/register/')
def lesson(request, pk):
    _lesson = get_object_or_404(Lesson, id=pk)
    return render(request, 'app/lesson.html', {'lesson': _lesson})


def get_streaming_lesson(request, pk: int):
    file, status_code, content_length, content_range = open_file(request, pk)
    response = StreamingHttpResponse(file, status=status_code, content_type='video/mp4')

    response['Accept-Ranges'] = 'bytes'
    response['Content-Length'] = str(content_length)
    response['Cache-Control'] = 'no-cache'
    response['Content-Range'] = content_range
    return response


def update_position(request):
    if request.method == 'POST':
        data = json.loads(request.body)

        position = int(data['position'])
        lesson_id = int(data['lesson_id'])

        lesson = Lesson.objects.get(pk=lesson_id)
        duration_seconds = lesson.duration_seconds

        user = request.user
        lesson_view = LessonView.objects.get(user=user, lesson=lesson)
        lesson_view.updated_at = timezone.now()
        lesson_view.viewed_time_seconds = position

        if (position / duration_seconds) >= 0.8:
            # Устанавливаем поле viewed в True
            lesson_view.is_viewed = True

        lesson_view.save()

        return JsonResponse({'message': "You've watched the video!"})
    else:
        return JsonResponse({'message': 'Invalid request method.'})






class LessonByProductView(generics.ListAPIView):
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        products = user.products.all()

        lesson_ids = []
        for product in products:
            lesson_ids.extend(product.lesson_set.values_list('id', flat=True))

        return Lesson.objects.filter(id__in=lesson_ids)





class UserRegistrationAPIView(generics.CreateAPIView):
    '''Регистрация'''

    serializer_class = UserRegistrationSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response({'message': 'User registered successfully'}, status=status.HTTP_201_CREATED, headers=headers)

