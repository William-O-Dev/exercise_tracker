# Generated by Django 2.2 on 2021-07-01 17:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login_and_registration_app', '0013_remove_workout_exercises'),
    ]

    operations = [
        migrations.AddField(
            model_name='workout',
            name='exercises',
            field=models.ManyToManyField(related_name='added_exercises', to='login_and_registration_app.Exercise'),
        ),
    ]
