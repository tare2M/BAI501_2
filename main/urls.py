from django.urls import path
from.import views
from django.views.generic import TemplateView

from . import views

app_name="main"

urlpatterns = [
    path('', views.index, name='index'),
    path('processed', views.processed, name='processed'),
    path('edit', views.edit, name='edit'),
    path('edit2', views.edit2, name='edit2'),
    path('add1/', views.add1, name='add1'),
    path('add2/', views.add2, name='add2'),
    path('add1/addform1/', views.addform1, name='addform1'),
    path('add2/addform2/', views.addform2, name='addform2'),
    #path('add/addheuristic/', views.addheuristic, name='addheuristic'),
    path('delete1/<int:id>', views.delete1, name='delete1'),
    path('delete2/<int:id>', views.delete2, name='delete2'),
    path('update/<int:id>', views.update, name='update'),
    path('update2/<int:id>', views.update2, name='update2'),
    path('update/updaterecord/<int:id>', views.updaterecord, name='updaterecord'),
    path('update/updaterecord2/<int:id>', views.updaterecord2, name='updaterecord2'),

    #path('index/', views.index, name="index"),
    #path('single/<slug:slug>', views.single, name="single"),
    #path('aboutus/', views.aboutus, name="aboutus"),
]