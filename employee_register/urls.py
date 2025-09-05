from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('employees/', views.employee_list, name='employee_list'),
    path('employees/create/', views.employee_create, name='employee_create'),
    path('employees/<str:emp_id>/edit/', views.employee_update, name='employee_update'),
    path('employees/<str:emp_id>/delete/', views.employee_delete, name='employee_delete'),
]
