from rest_framework import serializers
from .models import *
from django.contrib.auth.models import User


class LessonViewSerializer(serializers.ModelSerializer):
    '''Вывод статистики урока'''

    class Meta:
        model = LessonView
        fields = ['is_viewed', 'watched_at', 'current_position_sec']

class LessonSerializer(serializers.ModelSerializer):
    '''Вывод урока'''
    lesson = LessonViewSerializer(read_only=True, many=True)

    class Meta:
        model = Lesson
        fields = ['name', 'duration_seconds', 'lesson']


class ProductListSerializer(serializers.ModelSerializer):
    '''Вывод списка продуктов'''

    lessons = LessonSerializer(read_only=True, many=True)

    class Meta:
        model = Product
        fields = ['name', 'lessons']


class ProductDetailSerializer(serializers.ModelSerializer):
    '''Вывод продукта'''

    lessons = LessonSerializer(read_only=True, many=True)

    class Meta:
        model = Product
        fields = ['name', 'lessons']


class ProductAccessSerializer(serializers.ModelSerializer):
    '''Вывод доступных продуктов'''

    product = ProductListSerializer(read_only=True)

    class Meta:
        model = ProductAccess
        fields = ['product']



class ProductStatsSerializer(serializers.Serializer):
    '''Вывод статистики по продуктам'''

    id = serializers.IntegerField()
    name = serializers.CharField()
    viewed_lessons_count = serializers.IntegerField()
    total_viewing_time = serializers.IntegerField()
    total_users_product = serializers.IntegerField()
    acquisition_percentage = serializers.FloatField()


class UserRegistrationSerializer(serializers.ModelSerializer):
    '''Регистрация'''

    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'password', 'email']

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
            email=validated_data.get('email', ''),
        )
        return user