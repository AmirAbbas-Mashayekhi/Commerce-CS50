from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.db.models import F, Case, When, Max, DecimalField
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .forms import ListingForm

from .models import Listing, User


def index(request):
    active_listings = Listing.objects.filter(active=True).annotate(
        current_price=Case(
            # If there are bids, use the highest bid amount
            When(bids__isnull=False, then=Max('bids__amount')),
            
            # Otherwise, fall back to the `starting_bid`
            default=F('starting_bid'),
            output_field=DecimalField()
        )
    )
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
        if form.is_valid():
            Listing.objects.create(user=request.user, active=True, **form.cleaned_data)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/create_listing.html", {"form": form})
    else:
        form = ListingForm()
        return render(request, "auctions/create_listing.html", {"form": form})
