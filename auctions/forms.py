from django import forms
from .models import Auction

class AuctionForm(forms.Form):
    name = forms.CharField(
        label='Name',
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control form-group col-sm-8',
            'placeholder': 'Provide a title'
        }
        )
    )
    description = forms.CharField(
        label='Description',
        required=True,
        widget=forms.Textarea(attrs={
            'class': 'form-control form-group',
            'placeholder': 'Tell more about the product',
            'rows': '3'
        }
        )
    )
    price = forms.DecimalField(
        label='Price',
        required=False,
        initial=0.00,
        widget=forms.NumberInput(attrs={
            'class': 'form-control form-group col-sm-3',
            'placeholder': 'Estimated price (optional)',
            'min': '0.01',
            'max': '999999999.99',
            'step': '0.01'
        }
        )
    )
    starting_bid = forms.DecimalField(
        label='Starting Bid',
        required=True,
        widget=forms.NumberInput(attrs={
            'class': 'form-control form-group col-sm-3',
            'placeholder': 'Starting bid',
            'min': '0.01',
            'max': '99999999999.99',
            'step': '0.01'
        }
        )
    )
    category = forms.ChoiceField(
        choices=Auction.categories,
        label='Category',
        widget=forms.Select(attrs={
            'class': 'form-control form-group col-sm-3',
        })
    )
    image = forms.URLField(
        label='Image URL',
        required=False,
        initial='https://user-images.githubusercontent.com/52632898/161646398-6d49eca9-267f-4eab-a5a7-6ba6069d21df.png',
        widget=forms.TextInput(attrs={
            'class': 'form-control form-group col-sm-8',
            'placeholder': 'Image URL (optional)',
        }
        )
    )


class CommentForm(forms.Form):
    comment = forms.CharField(
        label='',
        required=True,
        widget=forms.Textarea(attrs={
            'class': 'form-control-md lead form-group col-sm-8',
            'rows': '2',
            'cols': '80',
            'placeholder': 'Comment',
        }
        )
    )

    