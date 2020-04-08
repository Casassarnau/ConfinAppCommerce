from django import forms
from shop import models
from localflavor.es.forms import ESIdentityCardNumberField

from shop.range import RangeSliderField


class ShopForm(forms.ModelForm):
    # TODO: Obtain latitude and longitude from the street in google maps.

    def clean_photo(self):
        photo = self.cleaned_data['photo']
        size = getattr(photo, '_size', 0)
        if size > settings.MAX_UPLOAD_SIZE:
            raise forms.ValidationError("Please keep photo size under %s. Current filesize %s" % (
                filesizeformat(settings.MAX_UPLOAD_SIZE), filesizeformat(size)))
        return photo

    CIF = ESIdentityCardNumberField(only_nif=False, label='', widget=forms.TextInput(attrs={'placeholder': 'CIF'}))

    meanTime= RangeSliderField(label="", minimum=0, maximum=60,  step=5, name="How many time does the user stay in your shop while shopping?" )

    class Meta:
        model = models.Shop
        fields = ['CIF', 'name', 'meanTime', 'secondaryCategories', 'services', 'photo']

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
