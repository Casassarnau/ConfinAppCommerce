from django import forms
from django.conf import settings
from django.template.defaultfilters import filesizeformat
from mapbox_location_field.forms import LocationField
from django.utils import timezone

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

    meanTime = RangeSliderField(label="", minimum=0, maximum=60,  step=5,
                               name="How many time does the user stay in your shop while shopping?")

    map = LocationField(map_attrs={"center": [2.1589899, 41.3887901], "marker_color": "#ba6b6c", 'zoom': 10})

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


class ScheduleForm(forms.ModelForm):
    startHour = forms.TimeField(required=True, label='When will you buy?',
                           initial='%02d:%02d' % (timezone.now().hour, timezone.now().minute))
    endHour = forms.TimeField(required=True, label='When will you buy?',
                           initial='%02d:%02d' % (timezone.now().hour, timezone.now().minute))

    class Meta:
        model = models.Schedule
        fields = ['day', 'startHour', 'endHour']
        exclude = ['shop']

