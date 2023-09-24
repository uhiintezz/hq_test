from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.core.validators import FileExtensionValidator


class Product(models.Model):
    '''Продукты'''
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='products')
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class ProductAccess(models.Model):
    '''Доступ к продуктам'''
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='products_access')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='accesses')

    def __str__(self):
        return f'{self.user} - {self.product}'


class Lesson(models.Model):
    '''Уроки'''

    name = models.CharField(max_length=100)
    duration_seconds = models.PositiveIntegerField()
    products = models.ManyToManyField(Product, related_name='lessons')
    file = models.FileField(
        upload_to='video/',
        validators=[FileExtensionValidator(allowed_extensions=['mp4'])]
    )

    def get_absolute_url(self):
        return reverse('lesson', kwargs={'pk': self.pk})

    def __str__(self):
        return self.name


class LessonView(models.Model):
    '''Просмотры уроков'''

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name='lesson')
    current_position_sec = models.IntegerField(default=0)
    is_viewed = models.BooleanField(default=False,)
    watched_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.user} - {self.lesson.name}'


