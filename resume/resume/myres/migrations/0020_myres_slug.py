# Generated by Django 4.0.2 on 2022-02-14 12:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myres', '0019_alter_myres_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='myres',
            name='slug',
            field=models.SlugField(max_length=255, null=True, unique=True),
        ),
    ]
