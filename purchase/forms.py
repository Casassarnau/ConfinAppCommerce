from django import forms
from django.utils import timezone

from shop import models
from shop.select_category import SelectCategoryField


class FilterForm(forms.Form):
    # services = SelectCategoryField(queryset=models.Service.objects.all())
    category = SelectCategoryField(queryset=models.PrimaryCategory.objects.all(), placeholder="Find a category ...", required=False, is_loading=False)
    service = SelectCategoryField(queryset=models.Service.objects.all(), placeholder="Find a service ...", required=False, is_loading=False)
    time = forms.TimeField(required=True, label='A quina hora vols anar a comprar?',
                           initial='%02d:%02d' % (timezone.now().hour, timezone.now().minute))
    location = forms.CharField(required=True, widget=forms.TextInput(attrs={'placeholder': 'Clica\'m!',
                                                                            'readonly': 'True'}))

    def clean(self):
        return self.cleaned_data

    def clean_time(self):
        time = self.cleaned_data['time']
        if time < timezone.now().time():
            raise forms.ValidationError('Outdated')
        return time

    class Meta:
        fields = ['category', 'service', 'time']
