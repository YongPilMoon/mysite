from django import forms


class AlbumForm(forms.Form):
    title = forms.CharField(
         max_length=20,
    )
    description = forms.CharField(
        widget=forms.Textarea,
        label=""
    )


class PhotoForm(forms.Form):
    title = forms.CharField(
        max_length=20,
    )
    description = forms.CharField(
        widget=forms.Textarea,
        label=""
    )
    img = forms.ImageField(
    )
