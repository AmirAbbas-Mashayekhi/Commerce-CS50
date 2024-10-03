import decimal
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError, transaction
from django.db.models import F, Case, When, Max, DecimalField
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse

from .forms import BidForm, CommentForm, ListingForm

from .models import Bid, Comment, Listing, User, WatchList, Winner


def index(request):
    active_listings = Listing.objects.filter(active=True)
    return render(
        request,
        "auctions/index.html",
        {"active_listings": active_listings},
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


@login_required
def create_listing(request):
    if request.method == "POST":
        form = ListingForm(request.POST)
        bid_form = BidForm(request.POST)

        if form.is_valid() and bid_form.is_valid():

            with transaction.atomic():
                # Create Listing object
                listing = Listing.objects.create(
                    user=request.user, active=True, **form.cleaned_data
                )

                # Create Bid object as the starting bid
                Bid.objects.create(
                    user=request.user,
                    listing=listing,
                    amount=bid_form.cleaned_data["amount"],
                )
                return HttpResponseRedirect(reverse("index"))
        else:
            return render(
                request,
                "auctions/create_listing.html",
                {"form": form, "bid_form": bid_form},
            )
    else:
        form = ListingForm()
        bid_form = BidForm()
        return render(
            request,
            "auctions/create_listing.html",
            {"form": form, "bid_form": bid_form},
        )


def listing_detail(request, pk):
    is_anon_user = request.user.is_anonymous
    bidding_form = BidForm()
    comment_form = CommentForm()

    listing = get_object_or_404(Listing, pk=pk)
    comments = Comment.objects.filter(listing=listing)

    # Check if user is the one who created this listing
    is_owner = request.user == listing.user

    # Check if user is the winner
    is_winner = False if is_anon_user else Winner.objects.filter(user=request.user, listing=listing).exists()

    return render(
        request,
        "auctions/listing_detail.html",
        {
            "bidding_form": bidding_form,
            "comment_form": comment_form,
            "listing": listing,
            "comments": comments,
            "is_winner": is_winner,
            "is_owner": is_owner,
            "is_in_watch_list": (
                False
                if is_anon_user
                else WatchList.objects.filter(
                    user=request.user, listing=listing
                ).exists()
            ),
        },
    )


@login_required
def add_to_watch_list(request):
    listing_id = request.POST.get("listing_id")
    try:
        listing = Listing.objects.get(pk=listing_id)
    except Listing.DoesNotExist:
        return render(
            request,
            "auctions/error.html",
            {"code": 404, "message": "Listing not found"},
        )
    try:
        WatchList.objects.create(user=request.user, listing=listing)
    except IntegrityError:
        return render(
            request,
            "auctions/error.html",
            {"code": 400, "message": "Listing Already in WatchList."},
        )

    return HttpResponseRedirect(reverse("listing-detail", args=[listing_id]))


@login_required
def remove_from_watch_list(request):
    listing_id = request.POST.get("listing_id")
    try:
        listing = Listing.objects.get(pk=listing_id)
    except Listing.DoesNotExist:
        return render(
            request,
            "auctions/error.html",
            {"code": 404, "message": "Listing not found"},
        )

    try:
        watch_list = WatchList.objects.get(user=request.user, listing=listing)
        watch_list.delete()
    except IntegrityError:
        return render(
            request, "auctions/error.html", {"code": 400, "message": "Bad Request"}
        )
    return HttpResponseRedirect(reverse("listing-detail", args=[listing_id]))


@login_required
def add_bid(request):
    listing_id = request.POST.get("listing_id")
    amount = request.POST.get("amount")

    # Ensure amount is numeric
    try:
        amount = round(decimal.Decimal(amount), 2)
    except decimal.InvalidOperation:
        return render(
            request,
            "auctions/error.html",
            {"code": 400, "message": "Bid value must be numeric and monetary."},
        )

    listing = get_object_or_404(Listing, pk=listing_id)

    # Check if the bid is greater than the current price
    if amount <= listing.current_price():
        return render(
            request,
            "auctions/error.html",
            {"code": 400, "message": "The bid must be greater than the current price."},
        )

    # Create the bid
    try:
        Bid.objects.create(listing=listing, amount=amount, user=request.user)
        return HttpResponseRedirect(reverse("listing-detail", args=[listing.id]))
    except IntegrityError:
        return render(
            request,
            "auctions/error.html",
            {"code": 500, "message": "Can't create bid."},
        )


@login_required
def close_auction(request):
    listing = get_object_or_404(Listing, pk=request.POST.get("listing_id"))
    user = request.user

    # Check if the user making the request is the listing owner
    if listing.user != user:
        return render(request, "error.html", {"code": 403, "message": "forbidden"})

    # Closing the auction
    with transaction.atomic():
        # Deactivate listing
        listing.active = False
        listing.save()

        # Get the highest bid's user
        winner_user = Bid.objects.get(
            listing=listing, amount=listing.current_price()
        ).user

        # Create a new winner record for that user
        Winner.objects.create(user=winner_user, listing=listing)

    return HttpResponseRedirect(reverse("listing-detail", args=[listing.id]))


@login_required
def add_comments(request):
    listing = get_object_or_404(Listing, pk=request.POST.get("listing_id"))
    user = request.user
    text = request.POST.get("text")

    # Create Comment Object
    Comment.objects.create(user=user, listing=listing, text=text)

    return HttpResponseRedirect(reverse("listing-detail", args=[listing.id]))
