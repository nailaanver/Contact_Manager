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
    
    
    # ✅ Password Reset URLs
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='password_reset.html'), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'), name='password_reset_complete'),
]