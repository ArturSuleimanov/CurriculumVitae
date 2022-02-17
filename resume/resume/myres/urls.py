from django.urls import path
from .views import *
urlpatterns = [
    path("", HomePage.as_view(), name = 'home'),
    path("registration/", RegisterUser.as_view(), name = 'registration' ),
    path("auth/", Auth.as_view(), name = "autentification"),
    path('logout/', login_out, name= 'logout'),
    path('edit_inf/<slug:post_slug>/', EditBio.as_view(), name = 'edit_biography'),
    path('password-change/', PasswordChange.as_view(), name='password_change'),
    path('edit_pro/<slug:post_slug>', UpdateProfile.as_view(),name = "update_profile"),
    path('remove_user/', remove_user, name = 'remove_user'),
    path('about/', about, name ='about'),
    path('add_certificate/', AddCer.as_view(), name = 'add_certificate'),
    path('certificates/<int:user_id>', CerPage.as_view(), name = 'certificates'),
    path('certificates/<int:user_id>/del_certificate/<int:cer_id>', delete_certificate, name = 'delete_certificate'),
    path('profile/<slug:user_slug>', UserProfile.as_view(), name = 'profile'),
    path('search/', SearchResultsView.as_view(), name = 'search')

]