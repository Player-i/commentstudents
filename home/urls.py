from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("register/", views.register, name="register"),
    path('create/', views.create_post, name='create_post'),
    path('login/', views.user_login, name='login'),
    path('<int:post_id>/add_comment/', views.add_comment, name='add_comment'),
    path('<int:post_id>/', views.post_detail, name='post_detail'),
    path('logout/', views.logout_view, name='logout'),
    path('search_post/', views.search_post, name='search_post'),
    path('top/', views.top, name='top')
]
