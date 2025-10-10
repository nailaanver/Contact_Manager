from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_View, name='login'),
    path('register/', views.register, name='register'),
    path('logout/', views.logout_view, name='logout'),  # ✅ important
    path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('dashboard/', views.user_dashboard, name='dashboard'),
    path('add-contact/', views.add_contact, name='add_contact'),
    path('delete-contact/<int:id>/', views.delete_contact, name='delete_contact'),
    path('edit-contact/<int:pk>/', views.edit_contact, name='edit_contact'),
    path('profile/', views.profile_view, name='profile')
]