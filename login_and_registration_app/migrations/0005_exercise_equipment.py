# Generated by Django 2.2 on 2021-06-29 11:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login_and_registration_app', '0004_auto_20210628_1259'),
    ]

    operations = [
        migrations.AddField(
            model_name='exercise',
            name='equipment',
            field=models.CharField(default='', max_length=255),
            preserve_default=False,
        ),
    ]