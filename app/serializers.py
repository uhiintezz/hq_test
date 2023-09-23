from rest_framework import serializers
from .models import *
from django.contrib.auth.models import User
from .models import Lesson, LessonView





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




class LessonViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = LessonView
        fields = ['viewed_time_seconds', 'is_viewed', 'updated_at']



class LessonSerializer(serializers.ModelSerializer):
    views = LessonViewSerializer(many=True, read_only=True)

    class Meta:
        model = Lesson
        fields = ['id', 'name', 'duration_seconds', 'file', 'views']