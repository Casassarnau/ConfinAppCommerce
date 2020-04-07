from django.forms import ModelForm
from shop import models
from localflavor.es.forms import ESIdentityCardNumberField


class ShopForm(ModelForm):
    # TODO: Validation of the CIF.
    # TODO: Obtain latitude and longitude from the street in google maps.
    CIF = ESIdentityCardNumberField(only_nif=False)

    class Meta:
        model = models.Shop
        fields = ['CIF', 'name', 'meanTime']
        fieldsets = (
            ('Shop', {'fields': ('CIF', 'name', 'meanTime')}),
            ('location', {'fields': ('latitude', 'longitude')}),
        )

        labels = {
            'CIF': 'CIF',
            'name': 'Name',
            'meanTime': 'How many time does the user stay in your shop while shopping?'
        }

        help_text = {
            'CIF': 'CIF',
            'name': 'Name',
            'meanTime': 'How many time does the user stay in your shop while shopping?'
        }

        exclude = ['latitude', 'longitude']

