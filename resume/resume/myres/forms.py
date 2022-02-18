from captcha.fields import CaptchaField
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm, UserChangeForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.forms import HiddenInput
import re
from .models import *

def validate_username(value):
    """
    Checks valid symbols of username
    """
    pattern = re.compile( r"[A-Za-z0-9_]+")
    if not pattern.fullmatch(value):
        raise ValidationError(
            (f'{value} содержит недопустимые символы.'),
            params={'value': value},
        )



class RegistrationUserForm(UserCreationForm):
    """
    Класс формы регистрации
    """
    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={"class": 'input-form'}),  validators=[validate_username])
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={"class": 'input-form'}))
    password2 = forms.CharField(label='Повторите пароль', widget=forms.PasswordInput(attrs={"class": 'input-form'}))
    email = forms.EmailField(label="Email", widget=forms.EmailInput(attrs={"class": 'input-form'}))
    first_name = forms.CharField(label='Имя', widget=forms.TextInput(attrs={"class": 'input-form'}))
    last_name = forms.CharField(label='Фамилия', widget=forms.TextInput(attrs={"class": 'input-form'}))
    captcha = CaptchaField(label='Докажите, что вы не робот')


    class Meta:
        model = User
        fields = ('username','first_name', 'last_name', 'password1', 'password2', 'email')
        widgets = {
            'username': forms.TextInput(attrs={"class": 'input-form'}),
            'password1': forms.PasswordInput(attrs={"class": 'input-form'}),
            'password2' : forms.PasswordInput(attrs={"class": 'input-form'}),
            'first_name': forms.TextInput(attrs={"class": 'input-form'}),
            'last_name': forms.TextInput(attrs={"class": 'input-form'}),

        }




class UserAuthForm(AuthenticationForm):
    """
    Класс формы авторизации
    """
    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={"class": 'input-form'}))
    password = forms.CharField(label="Пароль", widget=forms.PasswordInput(attrs={"class": 'input-form'}))
    captcha = CaptchaField(label='Докажите, что вы не робот')


class UpdateProfileForm(forms.ModelForm):
    """
    Класс изменения биографии
    """
    about_me = forms.CharField(required=False, label = 'О себе', widget = forms.Textarea(attrs={'cols': 60, 'rows': 10, 'class': 'input-form area'}),)
    birthday = forms.DateField(required=False, label = 'Дата рождения', widget = forms.DateInput(attrs={'class': 'input-form'}),)
    mobile_number = forms.CharField(required=False, label = 'Телефон',widget= forms.TextInput(attrs={'class': 'input-form'}),)
    hobby =forms.CharField(required=False, label = 'Хобби', widget=forms.Textarea(attrs={'cols': 60, 'rows': 10, 'class': 'input-form area'}),)
    education = forms.CharField(required=False, label='Образование', widget=forms.Textarea(attrs={'cols': 60, 'rows': 10, 'class': 'input-form area'}),)
    working_experience = forms.CharField(required=False, label='Опыт работы', widget=forms.Textarea(attrs={'cols': 60, 'rows': 10, 'class': 'input-form area'}),)
    skills = forms.CharField(required=False, label='Навыки', widget=forms.Textarea(attrs={'cols': 60, 'rows': 10, 'class': 'input-form area'}),)
    photo =forms.ImageField(required=False, label= 'Фото', widget= forms.FileInput(attrs={'class': 'input-form file-input'}), )


    class Meta:
        model = Myres
        fields = ["birthday", 'mobile_number', 'email','about_me',  'hobby', 'education', 'working_experience', 'skills', 'photo']
        widgets = {
            'about_me': forms.Textarea(attrs={'cols': 60, 'rows': 10, 'class': 'input-form area'}),
            'birthday': forms.DateInput(attrs={'class': 'input-form'}),
            'mobile_number': forms.TextInput(attrs={'class': 'input-form'}),
            'email': forms.EmailInput(attrs={'class': 'input-form'}),
            'hobby': forms.Textarea(attrs={'cols': 60, 'rows': 10, 'class': 'input-form area'}),
            'education': forms.Textarea(attrs={'cols': 60, 'rows': 10, 'class': 'input-form area'}),
            'working_experience': forms.Textarea(attrs={'cols': 60, 'rows': 10, 'class': 'input-form area'}),
            'skills': forms.Textarea(attrs={'cols': 60, 'rows': 10, 'class': 'input-form area'}),
            'photo': forms.FileInput(attrs={'class': 'input-form file-input'})
        }



class ChangePassForm(PasswordChangeForm):
    """
    Форма для смены пароля пользователя
    """
    old_password = forms.CharField(label="Старый пароль", widget=forms.PasswordInput(attrs={"class": 'input-form'}))
    new_password1 = forms.CharField(label="Новый пароль", widget=forms.PasswordInput(attrs={"class": 'input-form'}))
    new_password2 = forms.CharField(label="Подтверждение пароля", widget=forms.PasswordInput(attrs={"class": 'input-form'}))
    captcha = CaptchaField(label='Докажите, что вы не робот')


class UserEditForm(forms.ModelForm):
    """
    Форма для изменения личной информации пользователя
    """
    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={"class": 'input-form'}),  validators=[validate_username])
    email = forms.EmailField(label="Email", widget=forms.EmailInput(attrs={"class": 'input-form'}))
    first_name = forms.CharField(label='Имя', widget=forms.TextInput(attrs={"class": 'input-form'}))
    last_name = forms.CharField(label='Фамилия', widget=forms.TextInput(attrs={"class": 'input-form'}))


    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', )





class RemoveUser(forms.Form):
    username = forms.CharField(label='Введите свой логин, чтобы подтвердить удаление', widget=forms.TextInput(attrs={"class": 'input-form'}))
    captcha = CaptchaField(label='Докажите, что вы не робот')




class AddCertificate(forms.ModelForm):
    """
    Certificates adding
    """
    photo =forms.ImageField(label= 'Сертификат', widget= forms.FileInput(attrs={'class': 'input-form file-input'}), )
    user = forms.IntegerField(widget=forms.HiddenInput, required=False)
    class Meta:
        model = Certificates
        fields = ['photo', 'user']



