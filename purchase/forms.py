from django import forms
from django.utils import timezone

from shop import models


class FilterForm(forms.Form):
    category = forms.ModelMultipleChoiceField(queryset=models.PrimaryCategory.objects.all(), required=False)
    service = forms.ModelMultipleChoiceField(queryset=models.Service.objects.all(), required=False)
    time = forms.TimeField(required=True, label='When will you buy?',
                           initial='%02d:%02d' % (timezone.now().hour, timezone.now().minute))

    def clean(self):
        return self.cleaned_data

    def clean_time(self):
        time = self.cleaned_data['time']
        if time < timezone.now().time():
            raise forms.ValidationError('Outdated')
        return time

    class Meta:
        fields = ['category', 'service', 'time']
