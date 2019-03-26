from django import forms

from post.models import NoticeComment, PostComment, ReportComment


class NoticeCommentForm(forms.ModelForm):
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
        model = NoticeComment
        fields = ("username", "comment", )


class PostCommentForm(forms.ModelForm):
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
        model = PostComment
        fields = ("username", "comment", )


class ReportCommentForm(forms.ModelForm):
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
        model = ReportComment
        fields = ("username", "comment", )
