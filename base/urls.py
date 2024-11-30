from django.urls import path
from . import views

urlpatterns = [
    # Authentication
    path("login/", views.login_page, name="login"),
    path("logout/", views.logout_user, name="logout"),
    path("register/", views.register_user, name="register"),
    path("activate/<uidb64>/<token>/", views.activate, name="activate"),
    path("forgot-password/", views.forgot_password, name="forgot_password"),
    path(
        "reset-password-validate/<uidb64>/<token>/",
        views.reset_password_validate,
        name="reset_password_validate",
    ),
    path("reset-password/", views.reset_password, name="reset_password"),

    # Home
    path("", views.home, name="home"),
    path("topics/", views.topics_page, name="topics_page"),
    path("activity/", views.activity_page, name="activity_page"),
    path("edit-user/", views.edit_user, name="edit_user"),
    path("profile/<str:pk>/", views.user_profile, name="user_profile"),

    # Room CRUD
    path("room/<str:pk>/", views.room, name="room"),
    path("create-room/", views.create_room, name="create_room"),
    path("update-room/<str:pk>/", views.update_room, name="update_room"),
    path("delete-room/<str:pk>/", views.delete_room, name="delete_room"),

    # Message CRUD
    path("edit-message/<str:pk>/", views.edit_message, name="edit_message"),
    path("delete-message/<str:pk>/", views.delete_message, name="delete_message"),

    # Friend Request
    path("sent-friend-request/<str:pk>/",
         views.sent_friend_request, name="sent_friend_request"),
    path("respond-my-followers-request/<str:pk>/<str:action>/",
         views.respond_my_followers_request, name="respond_my_followers_request"),

    # others_follow-ers
    path("get-followers/<str:pk>/", views.get_followers, name="get_followers"),
    path("get-following/<str:pk>/", views.get_following, name="get_following"),
    path("unfollow-user/<str:pk>/", views.unfollow_user, name="unfollow_user"),

    # my_follow-ers
    path("get-my-followers/", views.get_my_followers, name="get_my_followers"),
    path("get-my-following/", views.get_my_following, name="get_my_following"),
    path("unfollow-my-follower/<str:pk>/", views.unfollow_my_follower, name="unfollow_my_follower"),
    path("unfollow-my-following/<str:pk>/", views.unfollow_my_following, name="unfollow_my_following"),
]
