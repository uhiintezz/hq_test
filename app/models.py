from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.core.validators import FileExtensionValidator


class Product(models.Model):
    '''Продукты'''

    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='products')
    name = models.CharField(max_length=100)


class Lesson(models.Model):
    '''Уроки'''

    name = models.CharField(max_length=100)
    duration_seconds = models.PositiveIntegerField()
    products = models.ManyToManyField(Product)
    file = models.FileField(
        upload_to='video/',
        validators=[FileExtensionValidator(allowed_extensions=['mp4'])]
    )

    def get_absolute_url(self):
        return reverse('lesson', kwargs={'pk': self.pk})


class LessonView(models.Model):
    '''Просмотры уроков'''

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    viewed_time_seconds = models.IntegerField(default=0)
    is_viewed = models.BooleanField(default=False)
    updated_at = models.DateTimeField(default=None, null=True, blank=True)

    # Добавьте другие поля, если необходимо