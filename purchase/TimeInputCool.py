from django.forms import TimeInput


class TimeInputCool(TimeInput):
    format_key = 'TIME_INPUT_FORMATS'
    template_name = 'timecool.html'

