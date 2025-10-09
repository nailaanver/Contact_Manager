from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_View, name='login'),
    path('register/', views.register, name='register'),
    path('logout/', views.logout_view, name='logout'),  # ✅ important
    path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('dashboard/', views.user_dashboard, name='dashboard'),
    path('add-contact/', views.add_contact, name='add_contact'),

]