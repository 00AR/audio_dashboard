from django import forms
from .validator import validate_is_audio_file


class LoginForm(forms.Form):
    username = forms.CharField(max_length=50)


class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True


class MultipleFileField(forms.FileField):

    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleFileInput())
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        single_file_clean = super().clean
        if isinstance(data, (list, tuple)):
            result = [single_file_clean(d, initial) for d in data]
        else:
            result = single_file_clean(data, initial)
        return result


class MultiUploadAudioForm(forms.Form):
    files = MultipleFileField(validators=(validate_is_audio_file,))
