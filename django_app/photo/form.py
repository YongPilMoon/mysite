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


class MultiPhotoForm(forms.Form):
    title = forms.CharField(
        max_length=30,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
        })
    )
    description = forms.CharField(
        max_length=80,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
        })
    )
    img = forms.ImageField(widget=forms.ClearableFileInput(
                           attrs={
                               'multiple':True
                           }
                )
         )