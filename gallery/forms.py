from django import forms

from gallery.models import AlbumComment


class AlbumCommentForm(forms.ModelForm):
    username = forms.CharField(
        label="Username",
        required=True,
        widget=forms.TextInput(
            attrs={
                "placeholder": "Username",
                "required": "true"
            }))
    comment = forms.CharField(
        label="Comment",
        required=True,
        widget=forms.TextInput(
            attrs={
                "placeholder": "Comment",
                "required": "true"
            }))

    class Meta:
        model = AlbumComment
        fields = ("username", "comment", )
