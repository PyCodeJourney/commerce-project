from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class Category(models.Model):
    title = models.CharField(max_length=64)

    class Meta:
        ordering = ["title"]

    def __str__(self):
        return self.title


class Bid(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_bids")
    value = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.value}"


class Listing(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="owner")
    title = models.CharField(max_length=64)
    category = models.ForeignKey(
        Category,
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        related_name="category",
    )
    description = models.TextField()
    price = models.ForeignKey(Bid, on_delete=models.CASCADE, related_name="bids")
    image = models.ImageField(upload_to="images", default="images\default.jpg")
    watchlist = models.ManyToManyField(User, blank=True, related_name="watchlist")
    is_active = models.BooleanField(default=True)
    created_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["title"]

    def __str__(self):
        return self.title


class Comment(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="user_comments"
    )
    listing = models.ForeignKey(
        Listing, on_delete=models.CASCADE, related_name="listing_comments"
    )
    body = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["created_on"]

    def __str__(self):
        return self.body
