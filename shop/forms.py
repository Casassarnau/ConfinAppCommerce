from django import forms
from django.forms import ModelForm

from shop import models
from localflavor.es.forms import ESIdentityCardNumberField

from shop.range import RangeSliderField


class ShopForm(ModelForm):
    # TODO: Obtain latitude and longitude from the street in google maps.
    CIF = ESIdentityCardNumberField(only_nif=False, label='', widget=forms.TextInput(attrs={'placeholder': 'CIF'}))

    meanTime= RangeSliderField(label="", minimum=0, maximum=60,  step=5, name="How many time does the user stay in your shop while shopping?" )

    class Meta:
        model = models.Shop
        fields = ['CIF', 'name', 'meanTime', 'secondaryCategories', 'services']

        labels = {
            'name': '',
        }

        help_text = {
            'CIF': 'CIF',
            'name': 'Name',
        }

        exclude = ['latitude', 'longitude']

        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Shop name'}),
        }



    def is_add_shop(self):
        return True
