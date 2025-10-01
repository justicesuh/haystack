from django.contrib import admin
from django.urls import path

from haystack.users import views as user_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', user_views.index),
    path('login/', user_views.login),
    path('logout/', user_views.logout),
]
