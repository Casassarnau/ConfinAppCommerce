import re

from django import forms
from django.utils.safestring import mark_safe


class SelectCategoryField(forms.ModelMultipleChoiceField):

    def __init__(self, *args, **kwargs):

        self.name = kwargs.pop('name', '')
        print("SELF select", self)

        copy_kwargs = kwargs.copy()
        del copy_kwargs['queryset']
        kwargs['widget'] = SelectCategory(self.name, *args, copy_kwargs)

        if 'label' not in kwargs.keys():
            kwargs['label'] = False

        super(SelectCategoryField, self).__init__(*args, **kwargs)


class SelectCategory(forms.SelectMultiple):

    def __init__(self, elem_name, *args, **kwargs):
        widget = super(SelectCategory, self).__init__(*args, **kwargs)
        self.elem_name = str(elem_name)
        self.template_name = 'select_category.html'
        self.option_template_name = 'select_category_option.html'
        self.option_template_hidden_name = 'select_category_option.html'

    def get_context(self, name, value, attrs):
        context = super().get_context(name, value, attrs)
        context['widget']['optgroups'] = self.optgroups(name, context['widget']['value'], attrs)
        return context

    def render(self, name, value, attrs=None, renderer=None):
        context = self.get_context(name, value, attrs)
        s = self._render(self.template_name, context, renderer)
        return mark_safe(s)