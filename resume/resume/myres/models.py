from django.contrib.auth.models import User, AbstractUser
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse
from phonenumber_field.modelfields import PhoneNumberField





class Myres(models.Model):
    """
    Модель для хранения биографии пользователя
    """
    user = models.OneToOneField(User, null=True, on_delete= models.CASCADE, related_name='profile')
    about_me = models.TextField(blank = True)
    birthday = models.DateField(auto_now=False, auto_now_add=False, null=True, blank = True)
    mobile_number = PhoneNumberField(unique = True, null = True, blank = True)
    email = models.EmailField(max_length=254, null=True)
    hobby = models.TextField(blank = True)
    education = models.TextField(blank = True)
    working_experience = models.TextField(blank = True)
    skills = models.TextField(blank = True)
    photo = models.ImageField(upload_to='photos/%Y/%m/%d/', blank = True)
    slug = models.SlugField(null = True, max_length=255, unique=True, db_index=True)

    # Следующие две функции будут создавать запись в модели Myres при создании нового пользователя
    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Myres.objects.create(user=instance, email=instance.email, slug =instance.username)


    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()


    def get_absolute_url(self): # Тут мы создали новый метод
        return reverse('home', args=[str(self.slug)])





