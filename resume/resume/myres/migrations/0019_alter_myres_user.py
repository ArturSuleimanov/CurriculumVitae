# Generated by Django 4.0.2 on 2022-02-14 11:20

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('myres', '0018_alter_myres_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='myres',
            name='user',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='profile', to=settings.AUTH_USER_MODEL),
        ),
    ]