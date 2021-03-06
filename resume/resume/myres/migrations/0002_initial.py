# Generated by Django 4.0.2 on 2022-02-13 15:45

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Myres',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('about_me', models.TextField()),
                ('birthday', models.DateField()),
                ('mobile_number', phonenumber_field.modelfields.PhoneNumberField(max_length=128, region=None, unique=True)),
                ('hobby', models.TextField()),
                ('education', models.TextField()),
                ('working_experience', models.TextField()),
                ('skills', models.TextField()),
                ('photo', models.ImageField(upload_to='photos/%Y/%m/%d/')),
                ('user', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
