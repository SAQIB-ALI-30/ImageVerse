from django.urls import path
from . import views

urlpatterns = [
    # path('', views.index, name='index'),
    path('', views.upload_list, name='upload_list'),
    path('create/', views.upload_create, name='upload_create'),
    path('<int:upload_id>/edit/', views.upload_edit, name='upload_edit'),
    path('<int:upload_id>/delete/', views.upload_delete, name='upload_delete'),
    path('register/', views.register, name='register'),
    path('logout/', views.user_logout, name='logout'),
    path('upload/search/', views.upload_search, name='upload_search'),
]