# Generated by Django 4.0.2 on 2022-02-14 08:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myres', '0005_alter_myres_photo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='myres',
            name='photo',
            field=models.ImageField(upload_to='photos/%Y/%m/%d/'),
        ),
    ]
