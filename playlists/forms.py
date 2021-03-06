from django import forms

from .models import Playlist

# class PlaylistForm(forms.Form):
#     title = forms.CharField()

class PlaylistModelForm(forms.ModelForm):
    #title = forms.CharField()
    class Meta:
        model = Playlist
        fields = [
            'title',
            'content',
        ]

    def clean_title(self):
        data = self.cleaned_data.get('title')
        if len(data) < 4:
            raise forms.ValidationError("This is not long enough")
        return data

    def clean_content(self):
        data = self.cleaned_data.get('content')
        if len(data) < 4:
            raise forms.ValidationError("This is not long enough")
        return data