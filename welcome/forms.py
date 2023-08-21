from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Post, Profile


class SearchForm(forms.Form):
    name = forms.CharField(label="Username", max_length=120)


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['bio', 'dp', 'gender', 'contact', 'dob']


class SignIn(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'password']



class PasswordForm(forms.ModelForm):
    new_password1 = forms.CharField(max_length=40)
    new_password2 = forms.CharField(max_length=40)

    class Meta:
        model = User
        fields = ["new_password1","new_password1"]



class SignUp(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=40)
    last_name = forms.CharField(max_length=40)

    class Meta:
        model = User
        fields = [
            'username', 'email', 'first_name',
            'last_name', 'password1', 'password2'
        ]

    def save(self, commit=True):
        user = super().save(commit=False)

        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']

        if commit:
            user.save()
        return user


class PostForm(forms.ModelForm):
    # widget = forms.Textarea(
    #     attrs={'rows': 3,

    class Meta:
        model = Post
        fields = ['title', 'description']
