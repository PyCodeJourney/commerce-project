from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from decimal import Decimal
import os

from .models import *


def index(request):
    return render(request, "auctions/index.html", {"listings": Listing.objects.all()})


def create_listing(request):
    if request.method == "POST":
        title = request.POST["title"]
        description = request.POST["description"]
        price = Bid.objects.create(user=request.user, value=request.POST["price"])
        if category_data := request.POST.get("category"):
            category_data = Category.objects.get(title=category_data)
        image = request.FILES.get("image")
        if not image:
            image = os.path.join(settings.MEDIA_ROOT, "images\default.jpg")
        listing = Listing.objects.create(
            user=request.user,
            title=title,
            description=description,
            price=price,
            category=category_data,
            image=image,
        )
        listing.save()
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(
            request,
            "auctions/create_listing.html",
            {"categories": Category.objects.all()},
        )

def close_listing(request, listing_id):
    listing = Listing.objects.get(pk=listing_id)
    listing.is_active = False
    listing.save()
    return HttpResponseRedirect(reverse("listing", args=(listing_id,)))


def listing(request, listing_id):
    listing = Listing.objects.get(pk=listing_id)
    return render(
        request,
        "auctions/listing.html",
        {"listing": listing, "comments": Comment.objects.filter(listing=listing)},
    )


def watchlist(request):
    return render(
        request, "auctions/watchlist.html", {"watchlist": request.user.watchlist.all()}
    )


def add_to_watchlist(request, listing_id):
    listing = Listing.objects.get(pk=listing_id)
    user = request.user
    listing.watchlist.add(user)
    return HttpResponseRedirect(reverse("listing", args=(listing_id,)))


def remove_from_watchlist(request, listing_id):
    listing = Listing.objects.get(pk=listing_id)
    user = request.user
    listing.watchlist.remove(user)
    return HttpResponseRedirect(reverse("listing", args=(listing_id,)))


def categories(request):
    return render(
        request, "auctions/categories.html", {"categories": Category.objects.all()}
    )


def category_view(request, category_id):
    category = Category.objects.get(pk=category_id)
    return render(
        request,
        "auctions/category.html",
        {"category": category, "listings": Listing.objects.filter(category=category)},
    )


def comment(request, listing_id):
    user = request.user
    body = request.POST["comment"]
    listing = Listing.objects.get(pk=listing_id)
    comment = Comment.objects.create(user=user, body=body, listing=listing)
    comment.save()
    return HttpResponseRedirect(reverse("listing", args=(listing_id,)))


def bid(request, listing_id):
    user = request.user
    value = request.POST["bid"]
    listing = Listing.objects.get(pk=listing_id)
    if Decimal(value) > listing.price.value:
        listing.price = Bid.objects.create(user=user, value=value)
        if not user in listing.watchlist.all():
            listing.watchlist.add(user)
        listing.save()
        return HttpResponseRedirect(reverse("listing", args=(listing_id,)))
    else:
        return render(
            request,
            "auctions/listing.html",
            {
                "listing": listing,
                "comments": Comment.objects.filter(listing=listing),
                "bid_error_message": "Please make sure that your Bid is greater than the current Price",
            },
        )

def login_view(request):
    if request.method == "POST":
        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(
                request,
                "auctions/login.html",
                {"message": "Invalid username and/or password."},
            )
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(
                request, "auctions/register.html", {"message": "Passwords must match."}
            )

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(
                request,
                "auctions/register.html",
                {"message": "Username already taken."},
            )
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")
