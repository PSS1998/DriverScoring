from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^matched/', views.matched, name='matched'),
    url(r'^$', views.index, name='index'),
]
