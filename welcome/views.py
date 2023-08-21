from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import redirect, render

from .forms import PasswordForm, PostForm, ProfileForm, SignUp
from .models import Friendship, Post, Profile


def start(request):
    return render(request, "welcome/start.html")


def signup(request):
    if request.method == "POST":
        form = SignUp(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get("username")
            user = User.objects.get(username=username)
            new_profile = Profile(user=user)
            new_profile.save()
            messages.success(request, "User has been registered.")
            return redirect("/signin/")
    else:
        form = SignUp()
    return render(request, "welcome/signup.html", {"form": form})


@login_required()
def update_profile(request):
    same_user = request.user
    if request.method == "POST":
        form = SignUp(request.POST)
        if form.is_valid():
            form.save()
            return render(request, "welcome/profileupdate.html")
    context = {"user": same_user}
    return render(request, "welcome/mainpage.html", context)


def signin(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("/profileview/")
        else:
            return render(request, "welcome/signin.html", {"form": form})

    form = AuthenticationForm()
    return render(request, "welcome/signin.html", {"form": form})


@login_required()
def mainpage(request):
    return render(request, "welcome/mainpage.html")


@login_required()
def auth_logout(request):
    logout(request)
    return redirect("welcome:start")


@login_required()
def profileview(request):
    form = Profile(request.POST)
    context_list = Profile.objects.all()
    profile = Profile.objects.get(user=request.user)
    context_dict = {
        "context_list": context_list,
        "form": form,
        "profile": profile,
    }
    return render(request, "welcome/profileview.html", context_dict)


@login_required()
def changepassword(request):
    if request.method == "POST":
        new_password1 = request.POST.get("new_password1")
        new_password2 = request.POST.get("new_password2")
        if new_password1 == new_password2:
            user = User.objects.get(username=request.user.username)
            user.set_password(new_password1)
            user.save()
            return HttpResponse("Password changed")
        else:
            return HttpResponse("Wrong Password")

    else:
        form = PasswordForm()
        context = {"form": form}
        return render(request, "welcome/changepassword.html", context)


@login_required()
def profileupdate(request):
    if request.method == "POST":
        form = ProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if form.is_valid():
            form.save()
        return redirect("/profileview/")
    form = ProfileForm(instance=request.user.profile)
    return render(request, "welcome/profileupdate.html", {"form": form})


@login_required()
def postcreate(request):
    form = PostForm(request.POST)
    if request.method == "POST":
        if form.is_valid():
            f1 = form.save(commit=False)
            f1.user = request.user
            f1.save()
        return redirect("welcome:postcreate")
    return render(request, "welcome/postcreate.html", {"form": form})


@login_required()
def main_post_view(request):
    form = PostForm(request.POST)
    if request.method == "POST":
        if form.is_valid():
            f1 = form.save(commit=False)
            f1.user = request.user
            f1.save()
        return redirect("welcome:main_post_view")

    sender = request.user
    friend = Q(sender=sender, status="Accept") | Q(receiver=sender, status="Accept")
    friends = Friendship.objects.filter(friend)
    friends_id = friends.values_list("sender__id", flat=True)
    self_id = friends.values_list("receiver__id", flat=True)

    allposts = Post.objects.all().order_by("-date_posted")
    context = {
        "allposts": allposts,
        "friends_id": friends_id,
        "self_id": self_id,
        "form": form,
    }
    return render(request, "welcome/mainpostview.html", context)


@login_required()
def postview(request):
    form = PostForm(request.POST)
    if request.method == "POST":
        if form.is_valid():
            f1 = form.save(commit=False)
            f1.user = request.user
            f1.save()
        return redirect("welcome:postview")
    allposts = Post.objects.all().order_by("-date_posted")
    return render(
        request, "welcome/postview.html", {"allposts": allposts, "form": form}
    )


@login_required()
def search(request):
    if request.method == "POST":
        query = request.POST.get("q")
        searcharea = Q(user__first_name__icontains=query) | Q(
            user__username__icontains=query
        )
        allprofile = Profile.objects.filter(searcharea)
        return render(request, "welcome/search.html", {"allprofile": allprofile})
    return render(request, "welcome/search.html")


@login_required()
def userprofile(request, profile_id):
    profile = Profile.objects.get(user_id=profile_id)
    try:
        context = Friendship.objects.get(
            sender=profile.user.id, receiver=request.user.id
        )
    except:
        context = Friendship.objects.filter(
            receiver=profile.user.id, sender=request.user.id
        )
    return render(
        request, "welcome/userprofile.html", {"profile": profile, "context": context}
    )


def friends(request):
    context = User.objects.all()
    check_status = Friendship.objects.all()
    return render(
        request,
        "welcome/friends.html",
        {"context": context, "check_status": check_status},
    )


@login_required()
def send_friend_request(request, userid):
    sender = request.user
    receiver = User.objects.get(id=userid)
    friend_request, created = Friendship.objects.get_or_create(
        sender=sender, receiver=receiver, status="Sent"
    )
    if created:
        context = Profile.objects.all()
        return redirect(request.META.get("HTTP_REFERER", {"context": context}))
    else:
        context = Profile.objects.all()
        return redirect(request.META.get("HTTP_REFERER", {"context": context}))


@login_required()
def friends_invites(request):
    friend = Friendship.objects.filter(receiver=request.user, status="Sent")
    return render(request, "welcome/friendsinvite.html", {"friend": friend})


@login_required()
def accept_friend(request, userid):
    receiver = request.user
    sender = User.objects.get(id=userid)
    friend_request = Friendship.objects.get(sender=sender, receiver=receiver)
    friend_request.status = "Accept"
    friend_request.save()
    return render(request, "welcome/friendlist.html")


@login_required()
def friend_list(request):
    friendlist = Friendship.objects.filter(
        Q(sender=request.user, status="Accept")
        | Q(receiver=request.user, status="Accept")
    )
    return render(request, "welcome/friendlist.html", {"friendlist": friendlist})


@login_required()
def remove_friend(request, userid):
    sender = request.user
    receiver = User.objects.get(id=userid)
    remove_friend = Friendship.objects.filter(
        Q(sender=sender, receiver=receiver, status="Accept")
        | Q(sender=receiver, receiver=sender, status="Accept")
    )
    remove_friend.delete()
    return redirect(request.META.get("HTTP_REFERER"))


@login_required()
def cancel_request(request, userid):
    sender = request.user
    receiver = User.objects.get(id=userid)
    cancel_request = Friendship.objects.filter(
        Q(sender=sender, receiver=receiver, status="Sent")
        | Q(sender=receiver, receiver=sender, status="Sent")
    )
    cancel_request.delete()
    return redirect(request.META.get("HTTP_REFERER"))
