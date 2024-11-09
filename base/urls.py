from django.urls import path
from .import views

urlpatterns = [
    #Authentication
    path('login/', views.login_page, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('register/', views.register_user, name='register'),
    path('activate/<uidb64>/<token>/', views.activate, name='activate'),
    path('forgot-password/', views.forgot_password, name='forgot_password'),
    path('reset-password-validate/<uidb64>/<token>/', views.reset_password_validate, name='reset_password_validate'),
    path('reset-password/', views.reset_password, name='reset_password'),

    #
    path('', views.home, name='home'),
    path('topics/', views.topics_page, name='topics_page'),
    path('activity/', views.activity_page, name='activity_page'),
    path('edit-user/', views.edit_user, name='edit_user'),
    path('profile/<str:pk>/', views.user_profile, name='user_profile'),

    # Room CRUD
    path('room/<str:pk>/', views.room, name='room'),
    path('create-room/', views.create_room, name='create_room'),
    path('update-room/<str:pk>/', views.update_room, name='update_room'),
    path('delete-room/<str:pk>/', views.delete_room, name='delete_room'),

    # Message
    path('edit-message/<str:pk>/', views.edit_message, name='edit_message'),
    path('delete-message/<str:pk>/', views.delete_message, name='delete_message'),
]
