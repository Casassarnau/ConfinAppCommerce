from django import forms
from django.template.defaultfilters import filesizeformat

from hackovid import settings
from shop import models
from localflavor.es.forms import ESIdentityCardNumberField


class ShopForm(forms.ModelForm):
    # TODO: Obtain latitude and longitude from the street in google maps.
    CIF = ESIdentityCardNumberField(only_nif=False)
    photo = forms.ImageField()

    def clean_photo(self):
        photo = self.cleaned_data['photo']
        size = getattr(photo, '_size', 0)
        if size > settings.MAX_UPLOAD_SIZE:
            raise forms.ValidationError("Please keep photo size under %s. Current filesize %s" % (
                filesizeformat(settings.MAX_UPLOAD_SIZE), filesizeformat(size)))
        return photo

    class Meta:
        model = models.Shop
        fields = ['CIF', 'name', 'meanTime', 'secondaryCategories', 'services', 'photo']

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

