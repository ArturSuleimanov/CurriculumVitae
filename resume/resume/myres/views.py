from django.contrib.auth import logout, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.views import LoginView, PasswordChangeView
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from .forms import *
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, ListView
from django.core.paginator import Paginator





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
    raise_exception = True



    def get_context_data(self, *, object_list=None, **kwargs):
        """
        Передача параметров в шаблон
        """
        context = super().get_context_data(**kwargs)
        context['title'], context['button_name'], context['action'] = 'Изменение резюме', 'Сохранить', 'edit_biography'
        return context


    def get_success_url(self):

        return reverse_lazy('profile', kwargs = {'user_slug':self.request.user.username})


    def get_object(self):
        """
        Не позволит пользователю редактировать никакую информацию кроме своей
        """
        return self.request.user.profile




class PasswordChange(LoginRequiredMixin, PasswordChangeView):
    """
    Класс представления для смены пароля пользователя
    """
    form_class = ChangePassForm
    template_name = 'myres/forms.html'
    success_url = reverse_lazy('home')
    raise_exception = True
    login_url = '/auth/'
    redirect_field_name = 'autentification'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'], context['button_name']= 'Смена пароля', 'Подтвердить'
        return context






class UpdateProfile(LoginRequiredMixin, UpdateView):
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


    def form_valid(self, form):
        my = Myres.objects.get(user_id = self.request.user.pk)
        my.name = self.request.user.first_name
        my.surname = self.request.user.last_name
        my.slug = self.request.user.username
        my.save()
        return super().form_valid(form)







@login_required(login_url='autentification')
def remove_user(request):
    """
    Удаление пользователя
    """
    if request.method == 'POST':
        form = RemoveUser(request.POST)
        if form.is_valid():
            rem = User.objects.get(username=form.cleaned_data['username'])

            if rem is not None and rem == request.user:
                rem.delete()
                return redirect('autentification')
            else:
                form.add_error(None, 'Введите свой логин')
    else:
        form = RemoveUser()
    context = {'form': form, 'index':'Удаление пользователя', 'button_name':"Удалить"}
    return render(request, 'myres/forms.html', context)



def about(request):
    return render(request, 'myres/about.html', {'title':'О сайте'})





class AddCer(LoginRequiredMixin, CreateView):
    """
    Класс представления для добавления сертификатов
    """
    login_url = '/auth/'
    redirect_field_name = 'autentification'
    form_class = AddCertificate
    model = Certificates
    template_name = 'myres/add_certificate.html'


    def form_valid(self, form):

        form.instance.user_id = self.request.user.pk
        return super().form_valid(form)


    def get_success_url(self):
        return reverse_lazy('certificates', kwargs = {'user_id':self.request.user.pk})


    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'], context['button_name'] = 'Загрузка сертификата', 'Сохранить'
        return context



class CerPage(ListView):
    """
    Страница с сертификатами
    """
    paginate_by = 5
    model = Certificates
    template_name = 'myres/certificates.html'
    context_object_name = 'posts'



    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title']= 'Сертификаты'
        return context


    def get_queryset(self, *args, **kwargs):
        user_id = self.kwargs.get('user_id')
        return Certificates.objects.filter(user_id = user_id)




@login_required(login_url='autentification')
def delete_certificate(request, user_id, cer_id):
    """
    Удаление сертификата
    """
    try:
        certificate = Certificates.objects.get(pk = cer_id)
        if certificate.user_id == request.user.pk:
            certificate.delete()
        return HttpResponseRedirect(f"/certificates/{user_id}")
    except certificate.DoesNotExist:
        return HttpResponseNotFound("<h1>Certificate not found</h1>")



class HomePage(ListView):
    """
    Домашняя страница
    """
    paginate_by = 5

    model = Myres
    template_name = 'myres/home.html'
    context_object_name = 'posts'


    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Главная страница'

        return context


    def get_queryset(self, *args, **kwargs):
        return Myres.objects.order_by('-time_create')






class UserProfile(ListView):
    model = Myres
    template_name = 'myres/profile.html'
    context_object_name = 'posts'


    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        print(f'{self.request.user.first_name} {self.request.user.last_name}')
        context['title'] = f'{self.request.user.first_name} {self.request.user.last_name}'
        return context


    def get_queryset(self, *args, **kwargs):
        user_slug = self.kwargs.get('user_slug')
        return Myres.objects.filter(slug = user_slug)


class SearchResultsView(ListView):
    '''
    Поиск пользователей по имени и фамилии
    '''
    paginate_by = 5
    model = Myres
    template_name = 'myres/home.html'
    context_object_name = 'posts'


    def get_queryset(self):
        """
        Обработка поискового запроса
        """
        query = self.request.GET.get('q')
        if not query:
            return Myres.objects.all()
        object_list = Myres.objects.filter(
            Q(name__icontains=query) | Q(surname__icontains=query)
        )
        return object_list


    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Результаты поиска'
        return context
