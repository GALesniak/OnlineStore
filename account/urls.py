from django.contrib import admin
from django.urls import path
from account.views import (
                                WelcomeView, UserRegistrationView, LoginView, LogoutUser,
)

app_name = 'account'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', WelcomeView.as_view(), name='index'),
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutUser.as_view(), name='logout'),

]

