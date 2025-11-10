from . import views
from django.urls import path

urlpatterns = [
    path('', views.home, name="home"),
    path('stocks', views.stocks, name="stocks"),
    path('login', views.login_view, name="login_view"),
    path('logout', views.logout_view, name="logout_view"),
    path('screening', views.screening, name="screening"),
    path('signup', views.signup_view, name="signup_view"),
    path('apps', views.apps, name='apps')

]