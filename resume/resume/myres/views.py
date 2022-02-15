from django.contrib.auth import logout, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.views import LoginView, PasswordChangeView
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404

from .forms import *
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView


def index(request):
    """
    Представление домашней страницы
    """
    if not request.user.is_authenticated:    # Перенаправление неавторизованного пользователя
        return redirect('autentification')
    return render(request, "myres/base.html", {'title':"Главная страница"})



def pageNotFound(request, exception):
    """
    Представление ошибки 404
    """
    return HttpResponseNotFound('<h1 style="text-align: center; color: blue; font-family: sans-serif;">Page not found</h1>')


class RegisterUser(CreateView):
    """
    Класс представления для регистрации пользователя
    """
    template_name = "myres/forms.html"
    success_url = reverse_lazy('autentification')
    form_class = RegistrationUserForm


    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'], context['button_name'] = 'Регистрация', 'Регистрация'
        return context


    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('home')



class Auth(LoginView):
    """
    Класс представления авторизации пользователя
    """
    form_class = UserAuthForm
    template_name = 'myres/forms.html'


    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'], context['button_name'] = 'Авторизация', "Войти"
        return context


    def get_success_url(self):
        """
        Перенаправление при успешной авторизации
        """
        return reverse_lazy('home')




def login_out(request):
    """
    Выход для авторизованного пользователя
    """
    logout(request)
    return redirect('autentification')








class EditBio(LoginRequiredMixin, UpdateView):
    """
    Класс представления для изменения информации о пользователе
    """
    model = Myres
    slug_url_kwarg = 'post_slug'
    template_name = 'myres/forms.html'

    form_class = UpdateProfileForm
    login_url = '/auth/'
    redirect_field_name = 'autentification'


    def get_context_data(self, *, object_list=None, **kwargs):
        """
        Передача параметров в шаблон
        """
        context = super().get_context_data(**kwargs)
        context['title'], context['button_name'] = 'Изменение резюме', 'Сохранить'
        return context


    def get_success_url(self):
        return reverse_lazy('home')


    def get_object(self):
        """
        Не позволит пользователю редактировать никакую информацию кроме своей
        """
        return self.request.user.profile




class PasswordChange(PasswordChangeView):
    """
    Класс представления для смены пароля пользователя
    """
    form_class = ChangePassForm
    template_name = 'myres/forms.html'
    success_url = reverse_lazy('home')
    raise_exception = True


    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'], context['button_name'] = 'Смена пароля', 'Подтвердить'
        return context






class UpdateProfile(UpdateView):
    """
    Изменение личной информации пользователя
    """
    model = User
    form_class = UserEditForm


    template_name = 'myres/edit_profile.html'
    slug_field = 'username'
    slug_url_kwarg = 'post_slug'
    login_url = '/auth/'
    redirect_field_name = 'autentification'


    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'], context['button_name'] = 'Настройки профиля', 'Сохранить'
        return context


    def get_success_url(self):
        return reverse_lazy('home')


    def get_object(self):
        return self.request.user




@login_required(login_url='http://127.0.0.1:8000/')
def remove_user(request):
    if request.method == 'POST':
        form = RemoveUser(request.POST)

        if form.is_valid():
            rem = User.objects.get(username=form.cleaned_data['username'])
            print(rem)

            if rem is not None and rem == request.user:
                rem.delete()
                return redirect('autentification')
            else:
                form.add_error(None, 'Введите свой логин')

    else:
        form = RemoveUser()
    context = {'form': form, 'index':'Удаление пользователя', 'button_name':"Удалить"}
    return render(request, 'myres/forms.html', context)