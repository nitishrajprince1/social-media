from django.urls import path

from . import views

app_name = "welcome"

urlpatterns = [
    path("", views.start, name="start"),
    path("signin/", views.signin, name="signin"),
    path("signup/", views.signup, name="signup"),
    path("mainpage/", views.mainpage, name="mainpage"),
    path("logout/", views.auth_logout, name="logout"),
    path("profileview/", views.profileview, name="profileview"),
    path("postcreate/", views.postcreate, name="postcreate"),
    path("postview/", views.postview, name="postview"),
    path("profileupdate/", views.profileupdate, name="profileupdate"),
    path("changepassword/", views.changepassword, name="changepassword"),
    path("search/", views.search, name="search"),
    path("friends/", views.friends, name="friends"),
    path(
        "sendfriendrequest/<int:userid>",
        views.send_friend_request,
        name="send_friend_request",
    ),
    path("accept_friend/<int:userid>", views.accept_friend, name="accept_friend"),
    path("userprofile/<int:profile_id>", views.userprofile, name="userprofile"),
    path("friendlist/", views.friend_list, name="friendlist"),
    path("remove_friend/<int:userid>", views.remove_friend, name="remove_friend"),
    path("cancel_request/<int:userid>", views.cancel_request, name="cancel_request"),
    path("friendsinvite/", views.friends_invites, name="friendsinvites"),
    path("mainpostview/", views.main_post_view, name="main_post_view"),
]
