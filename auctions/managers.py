from django.db import models
from django.db.models import Max, Case, When, F, DecimalField


class ListingQuerySet(models.QuerySet):
    def with_current_price(self):
        # Add an annotation for current_price (max bid or starting_bid)
        return self.annotate(
            current_price=Case(
                When(bids__isnull=False, then=Max("bids__amount")),
                default=F("starting_bid"),
                output_field=DecimalField(),
            )
        )


class ListingManager(models.Manager):
    def get_queryset(self):
        # Use the custom ListingQuerySet for all queries
        return ListingQuerySet(self.model, using=self._db).with_current_price()
