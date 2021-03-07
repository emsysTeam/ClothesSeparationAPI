from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('upload/', views.upload, name='upload'),
    path('list/', views.image_list, name='image_list'),
    path('show/<int:image_id>/', views.image_show, name='image_show')
]
