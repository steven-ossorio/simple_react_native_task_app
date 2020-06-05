from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login', views.login, name='login'),
    path('signup', views.signup, name='signup'),
    path('create_task', views.create_task, name='create_task'),
    path('delete_task', views.delete_task, name='delete_task'),
    path('update_task', views.update_task, name='update_task'),
    path('update_account', views.update_account, name='update_account')
]
