# Generated by Django 4.0.2 on 2022-02-14 10:08

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('myres', '0013_delete_myres'),
    ]

    operations = [
        migrations.CreateModel(
            name='Myres',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('about_me', models.TextField()),
                ('birthday', models.DateField()),
                ('mobile_number', phonenumber_field.modelfields.PhoneNumberField(max_length=128, null=True, region=None, unique=True)),
                ('email', models.EmailField(max_length=254, null=True)),
                ('hobby', models.TextField()),
                ('education', models.TextField()),
                ('working_experience', models.TextField()),
                ('skills', models.TextField()),
                ('photo', models.ImageField(upload_to='photos/%Y/%m/%d/')),
                ('user', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
