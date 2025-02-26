from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("listings", views.create_listing, name="create-listing"),
    path("listings/<int:pk>", views.listing_detail, name="listing-detail"),
    path("watchlists/add", views.add_to_watch_list, name="add-to-watch-list"),
    path(
        "watchlists/remove", views.remove_from_watch_list, name="remove-from-watch-list"
    ),
    path("bids/create", views.add_bid, name="add-bid"),
    path("listings/close", views.close_auction, name="close-auction"),
    path("comments/create", views.add_comments, name="add-comment"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("categories", views.categories, name="categories"),
    path("categories/<int:pk>", views.category_listings, name="category-listings"),
]
