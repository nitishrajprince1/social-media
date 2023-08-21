from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from django.utils import timezone

GENDER_CHOICES = (
    ("Male", "Male"),
    ("Female", "Female"),
    ("Not Specified", "Not Specified"),
)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    contact = models.IntegerField(blank=True, null=True)
    dob = models.DateField(null=True, blank=True)
    dp = models.ImageField(upload_to="profile_pics")
    bio = models.CharField(max_length=300)
    gender = models.CharField(max_length=50, choices=GENDER_CHOICES, default="Male")

    def __str__(self):
        return self.user.username


class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200, blank=True)
    date_posted = models.DateTimeField(default=timezone.now)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("post-detail", kwargs={"pk": self.pk})


status_choice = (
    ("A", "Accept"),
    ("S", "Sent"),
)


class Friendship(models.Model):
    status = models.CharField(max_length=50, choices=status_choice, blank=True)
    sender = models.ForeignKey(User, related_name="sender", on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, related_name="receive", on_delete=models.CASCADE)

    def __str__(self):
        return "{} by {}".format(self.sender, self.receiver)
