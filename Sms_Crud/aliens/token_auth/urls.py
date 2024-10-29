from django.urls import path
from . import views

urlpatterns=[
    path('',views.listview,name='std_list'),
    path('add/',views.add_std,name='std_create'),
    path('edit/<int:id>/',views.edit_std,name='std_edit'),
    path('delete/<int:id>/',views.del_std,name='std_delete'),
]