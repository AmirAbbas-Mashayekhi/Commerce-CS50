import decimal
from django import forms
from .models import Listing


class ListingForm(forms.ModelForm):
    class Meta:
        model = Listing
        fields = [
            "title",
            "description",
            "image_url",
            "category",
        ]
        widgets = {
            "title": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Enter title"}
            ),
            "description": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 5,
                    "placeholder": "Enter description",
                }
            ),
            "starting_bid": forms.NumberInput(
                attrs={"class": "form-control", "placeholder": "Enter starting bid"}
            ),
            "image_url": forms.URLInput(
                attrs={"class": "form-control", "placeholder": "Enter image URL"}
            ),
            "category": forms.Select(attrs={"class": "form-control"}),
        }


class AddBidForm(forms.Form):
    amount = forms.DecimalField(max_digits=7, decimal_places=2, min_value=decimal.Decimal(1.0))