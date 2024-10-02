from django.contrib import admin
from . import models


@admin.register(models.User)
class UserAdmin(admin.ModelAdmin):
    list_display = ["id", "username", "email"]
    search_fields = ["username__istartswith"]
    list_per_page = 20


@admin.register(models.Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["id", "title", "created_at", "listings_count"]
    search_fields = ["title__istartswith"]
    list_per_page = 10

    @staticmethod
    def listings_count(category):
        return category.listings.count()


@admin.register(models.Listing)
class ListingAdmin(admin.ModelAdmin):
    list_display = ["id", "active", "title", "category", "user"]
    list_editable = ["active"]
    search_fields = ["title__istartswith"]
    autocomplete_fields = ["category", "user"]
    list_per_page = 20


@admin.register(models.Bid)
class BidAdmin(admin.ModelAdmin):
    list_display = ["id", "listing", "user", "amount"]
    autocomplete_fields = ["listing", "user"]
    list_per_page = 20


@admin.register(models.WatchList)
class WatchListAdmin(admin.ModelAdmin):
    list_display = ["id", "user", "created_at"]
    autocomplete_fields = ["user", "listing"]
    list_per_page = 20


@admin.register(models.Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ["listing", "user", "created_at"]
    autocomplete_fields = ["listing", "user"]
    list_per_page = 20


@admin.register(models.Winner)
class WinnerAdmin(admin.ModelAdmin):
    list_display = ["listing", "user", "created_at"]
    autocomplete_fields = ["listing", "user"]
    list_per_page = 20
