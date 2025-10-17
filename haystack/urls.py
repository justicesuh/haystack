from django.contrib import admin
from django.urls import path

from haystack.jobs import views as job_views
from haystack.metrics import views as metric_views
from haystack.search import views as search_views
from haystack.users import views as user_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', metric_views.dashboard),
    path('login/', user_views.login),
    path('logout/', user_views.logout),
    path('jobs/', job_views.jobs),
    path('companies/', job_views.companies),
    path('searches/', search_views.searches),
]
