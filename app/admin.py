from django.contrib import admin
from .models import *


admin.site.register(ProductAccess)

class LessonAdmin(admin.ModelAdmin):
    list_display = ['name', 'duration_seconds']

class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'owner']


class LessonViewAdmin(admin.ModelAdmin):
    list_display = ['user', 'lesson', 'is_viewed']
    readonly_fields = ['watched_at']



admin.site.register(Product, ProductAdmin)
admin.site.register(Lesson, LessonAdmin)
admin.site.register(LessonView, LessonViewAdmin)