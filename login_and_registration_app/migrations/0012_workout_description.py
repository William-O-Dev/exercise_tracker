# Generated by Django 2.2 on 2021-06-30 23:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login_and_registration_app', '0011_workout_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='workout',
            name='description',
            field=models.TextField(default=''),
            preserve_default=False,
        ),
    ]