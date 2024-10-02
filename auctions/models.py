from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import Max
from django.core.validators import MinValueValidator


class User(AbstractUser):
    pass


class Category(models.Model):
    title = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.title


class Listing(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    image_url = models.URLField(blank=True, null=True)
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="listings")
    category = models.ForeignKey(
        Category,
        blank=True,
        null=True,
        on_delete=models.PROTECT,
        related_name="listings",
    )

    def current_price(self):
        highest_bid = self.bids.aggregate(Max("amount"))["amount__max"]
        return highest_bid if highest_bid is not None else 0

    def __str__(self) -> str:
        return self.title


class Bid(models.Model):
    amount = models.DecimalField(max_digits=7, decimal_places=2)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bids")
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="bids")

    def __str__(self) -> str:
        return f"{self.user} - {self.listing}"

    class Meta:
        unique_together = [["listing", "user", "amount"]]


class WatchList(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"{self.user} - {self.listing}"

    class Meta:
        unique_together = [["listing", "user"]]


class Comment(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"{self.user} - {self.listing}"


class Winner(models.Model):
    listing = models.OneToOneField(
        Listing, on_delete=models.CASCADE, related_name="winner"
    )
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="won_auctions"
    )
    created_at = models.DateTimeField(auto_now_add=True)
