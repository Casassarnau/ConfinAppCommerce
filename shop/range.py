
import re

from django import forms
from django.utils.safestring import mark_safe


class RangeSliderField(forms.CharField):

    def __init__(self, *args, **kwargs):
        self.name = kwargs.pop('name', '')
        self.minimum = kwargs.pop('minimum',0)
        self.maximum = kwargs.pop('maximum',10)
        self.step = kwargs.pop('step',1)

        kwargs['widget'] = RangeSlider(self.minimum, self.maximum, self.step, self.name)

        if 'label' not in kwargs.keys():
            kwargs['label'] = False

        super(RangeSliderField, self).__init__(*args, **kwargs)

class RangeSlider(forms.TextInput):

    def __init__(self, minimum, maximum, step, elem_name, *args,**kwargs):
        widget = super(RangeSlider,self).__init__(*args,**kwargs)
        self.minimum = str(minimum)
        self.maximum = str(maximum)
        self.step = str(step)
        self.elem_name = str(elem_name)

    def render(self, name, value, attrs=None, renderer=None):
        s = super(RangeSlider, self).render(name, value, attrs)
        self.elem_id = re.findall(r'id_([A-Za-z0-9_./\\-]*)"',s)[0]

        print("Render max:", self.maximum)
        html = """
        
        <label>"""+self.elem_name+"""</label>
        <div class="slider-container">
            <input id="slider-"""+self.elem_id+"""" type="range" value=0
            min="""+self.minimum+""" max="""+self.maximum+"""
            step="""+self.step+""" oninput="updateSliderLab(this.value)" onchange="updateSliderLab(this.value)">
            <div class="span-container">
                <span id="sliderLab-"""+self.elem_id+"""" >0 min</span>
            </div>
        </div>
        
        """
        return mark_safe(s+html)