import re

from django import forms
from django.utils.safestring import mark_safe


class SelectCategoryField(forms.ModelMultipleChoiceField):

    def __init__(self, *args, **kwargs):

        self.name = kwargs.pop('name', '')
        print("SELF select", self)

        placeholder = kwargs['placeholder']
        del kwargs['placeholder']

        is_loading = kwargs['is_loading']
        del kwargs['is_loading']

        title = kwargs['title']
        del kwargs['title']

        copy_kwargs = kwargs.copy()
        del copy_kwargs['queryset']
        kwargs['widget'] = SelectCategory(self.name, placeholder, is_loading, title, *args, copy_kwargs)

        if 'label' not in kwargs.keys():
            kwargs['label'] = False

        super(SelectCategoryField, self).__init__(*args, **kwargs)


class SelectCategory(forms.SelectMultiple):

    def __init__(self, elem_name, placeholder, is_loading, title, *args, **kwargs):
        widget = super(SelectCategory, self).__init__(*args, **kwargs)
        self.elem_name = str(elem_name)
        self.placeholder = placeholder
        self.is_loading = is_loading
        self.title = title
        self.template_name = 'select_category.html'
        self.option_template_name = 'select_category_option.html'
        self.option_template_hidden_name = 'select_category_option.html'

    def get_context(self, name, value, attrs):
        context = super().get_context(name, value, attrs)
        context['widget']['optgroups'] = self.optgroups(name, context['widget']['value'], attrs)
        context['widget']['placeholder'] = self.placeholder
        context['widget']['is_loading'] = self.is_loading
        context['widget']['title'] = self.title
        return context

    def render(self, name, value, attrs=None, renderer=None):
        context = self.get_context(name, value, attrs)
        s = self._render(self.template_name, context, renderer)
        return mark_safe(s)