from django import forms
from django.utils import timezone

from shop import models
from shop.select_category import SelectCategoryField


class FilterForm(forms.Form):
    category = SelectCategoryField(queryset=models.PrimaryCategory.objects.all(),
                                   placeholder="Buscar categoria...", required=False, is_loading=False, title="Filtra per categoria:")
    service = SelectCategoryField(queryset=models.Service.objects.all(),
                                  placeholder="Buscar servei...", required=False, is_loading=False, title="Filtra per servei:")
    time = forms.TimeField(required=True, label='A quina hora vols anar a comprar?',
                           initial='%02d:%02d' % ((timezone.now() + timezone.timedelta(minutes=30)).hour,
                                                  (timezone.now() + timezone.timedelta(minutes=30)).minute))
    location = forms.CharField(required=True, widget=forms.TextInput(attrs={'placeholder': 'Clica\'m!',
                                                                            'readonly': 'True'}))

    def clean(self):
        return self.cleaned_data

    # checks if time is not outdated
    def clean_time(self):
        time = self.cleaned_data['time']
        if time < timezone.now().time():
            raise forms.ValidationError('Outdated')
        return time

    class Meta:
        fields = ['category', 'service', 'time']
