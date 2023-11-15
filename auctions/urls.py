from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create", views.create_listing, name="create"),
    path("categories", views.categories, name="categories"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("categories/<int:category_id>", views.category_view, name="category"),
    path("<int:listing_id>", views.listing, name="listing"),
    path("<int:listing_id>/close", views.close_listing, name="close"),
    path(
        "<int:listing_id>/watchlist-add", views.add_to_watchlist, name="watchlist_add"
    ),
    path(
        "<int:listing_id>/watchlist-remove",
        views.remove_from_watchlist,
        name="watchlist_remove",
    ),
    path("<int:listing_id>/comment", views.comment, name="comment"),
    path("<int:listing_id>/bid", views.bid, name="bid"),
]
