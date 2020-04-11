from django import forms
from django.conf import settings
from django.template.defaultfilters import filesizeformat
from mapbox_location_field.forms import LocationField
from django.utils import timezone

from purchase.TimeInputCool import TimeInputCool
from shop import models
from localflavor.es.forms import ESIdentityCardNumberField
from shop.range import RangeSliderField
from shop.select_category import SelectCategoryField


class ShopForm(forms.ModelForm):

    def clean_photo(self):
        photo = self.cleaned_data['photo']
        if photo is None:
            raise forms.ValidationError("Siusplau, afegeix una fotografia")
        size = getattr(photo, '_size', 0)
        if size > settings.MAX_UPLOAD_SIZE:
            raise forms.ValidationError("Siusplau, la foto ha de tenir un tamany inferior a %s. Actualment %s" % (
                filesizeformat(settings.MAX_UPLOAD_SIZE), filesizeformat(size)))
        return photo

    CIF = ESIdentityCardNumberField(only_nif=False, label='', widget=forms.TextInput(attrs={'placeholder': 'CIF'}))
    secondaryCategories = SelectCategoryField(queryset=models.SecondaryCategory.objects.all(),
                                              placeholder='Busca una categoria ...', is_loading=False, title="Filtra per categoria:")
    services = SelectCategoryField(queryset=models.Service.objects.all(),
                                   placeholder='Busca un servei ...', is_loading=False, title="Filtra per servei:",
                                   required=False)

    meanTime = RangeSliderField(label="", minimum=0, maximum=60,  step=5,
                               name="Quant temps passen els teus usuaris de mitjana?")

    map = LocationField(label= 'Mapa', map_attrs={"center": [2.1589899, 41.3887901], "marker_color": "#ba6b6c", 'zoom': 10, 'placeholder':'Tria una localització a sota'})

    class Meta:
        model = models.Shop
        fields = ['CIF', 'name', 'description', 'meanTime', 'services', 'secondaryCategories', 'photo']

        labels = {
            'name': '',
            'description': '',
            'photo': 'Foto'
        }

        help_text = {
            'CIF': 'CIF',
            'name': 'Name',

        }

        exclude = ['latitude', 'longitude']

        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Nom de la botiga'}),
            'description': forms.Textarea(attrs={'rows': 4,'placeholder': 'Descripció'}),
            'photo': forms.FileInput(),
        }

    def clean(self):
        map = self.cleaned_data['map']
        if map is None:
            raise forms.ValidationError("Necesites unes coordenades")
        elif float(map.split(',')[0]) <= -180 or float(map.split(',')[0]) >= 180:
            raise forms.ValidationError("Longitude fora de rang")
        elif float(map.split(',')[1]) < -90 or float(map.split(',')[1]) >= 90:
            raise forms.ValidationError("Latitude fora de rang")
        else:
            pass
        return self.cleaned_data
      
    def is_add_shop(self):
        return True


class ScheduleForm(forms.ModelForm):
    startHour = forms.TimeField(required=True, label='Començament de la jornada',
                           initial='%02d:%02d' % (timezone.now().hour, timezone.now().minute), widget=TimeInputCool())
    endHour = forms.TimeField(required=True, label='Fi de la jornada',
                           initial='%02d:%02d' % (timezone.now().hour, timezone.now().minute), widget=TimeInputCool())

    class Meta:
        model = models.Schedule
        fields = ['day', 'startHour', 'endHour']
        exclude = ['shop']
        labels ={
            'day':'Dia'
        }

    def clean(self):
        day = self.cleaned_data['day']
        startHour = self.cleaned_data['startHour']
        endHour = self.cleaned_data['endHour']
        if startHour > endHour:
            raise forms.ValidationError('L\'hora d\'inici no pot ser més gran que la hora final')
        return self.cleaned_data


class AddShopAdminForm(forms.Form):
    email = forms.EmailField(required=True, label='', widget=forms.EmailInput(attrs={'placeholder': 'Correu electrònic'}))
