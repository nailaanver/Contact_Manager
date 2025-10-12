from django.urls import path
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('', views.login_View, name='login'),
    path('register/', views.register, name='register'),
    path('logout/', views.logout_view, name='logout'),  # ✅ important
    path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('dashboard/', views.user_dashboard, name='dashboard'),
    path('add-contact/', views.add_contact, name='add_contact'),
    path('delete-contact/<int:id>/', views.delete_contact, name='delete_contact'),
    path('edit-contact/<int:pk>/', views.edit_contact, name='edit_contact'),
    path('manage-contact/', views.manage_contact, name='manage_contact'),
    path('manage-users/', views.manage_users, name='manage_users'),
    path('edit_user/<int:pk>/',views.edit_user,name = 'edit_user'),
    path('delete_user/<int:id>/',views.delete_user,name = 'delete_user'),
    path('dashboard_content/', views.dashboard_content, name='dashboard_content'),
    path('profile/', views.profile_view, name='profile'),
    
    path('forgot-password/', views.forgot_password, name='forgot_password'),
    path('reset-password/<str:username>/', views.reset_password, name='reset_password'),

    
]