# Generated by Django 4.2.5 on 2023-09-22 19:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lessonview',
            name='viewed_time_seconds',
            field=models.IntegerField(default=0),
        ),
    ]