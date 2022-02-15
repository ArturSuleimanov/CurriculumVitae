from django.urls import path
from .views import *
urlpatterns = [
    path("", index, name = 'home'),
    path("registration/", RegisterUser.as_view(), name = 'registration' ),
    path("auth/", Auth.as_view(), name = "autentification"),
    path('logout/', login_out, name= 'logout'),
    path('edit_inf/<slug:post_slug>/', EditBio.as_view(), name = 'editbiography'),
    path('password-change/', PasswordChange.as_view(), name='password_change'),
    path('edit_pro/<slug:post_slug>', UpdateProfile.as_view(),name = "update_profile"),
    path('remove_user/', remove_user, name = 'remove_user')

]