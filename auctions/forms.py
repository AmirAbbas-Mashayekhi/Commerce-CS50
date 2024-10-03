import decimal
from django import forms
from .models import Comment, Listing


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
            "image_url": forms.URLInput(
                attrs={"class": "form-control", "placeholder": "Enter image URL"}
            ),
            "category": forms.Select(attrs={"class": "form-control"}),
        }


class BidForm(forms.Form):
    amount = forms.DecimalField(
        max_digits=7,
        decimal_places=2,
        min_value=decimal.Decimal(1.0),
        widget=forms.NumberInput(
            attrs={"class": "form-control", "placeholder": "Enter bid"}
        ),
    )


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["text"]
        widgets = {
            "text": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 5,
                    "placeholder": "Comment...",
                }
            ),
        }
