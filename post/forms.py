from django import forms

from post.models import Notice, Post, Report, NoticeComment, PostComment, ReportComment


class NoticeAddForm(forms.ModelForm):
    user = forms.CharField(
        label="E-mail",
        disabled=True,
        widget=forms.TextInput(
            attrs={
                "placeholder": "E-mail",
                "required": True,
            }))

    class Meta:
        model = Notice
        fields = ("user", "title", "photo", "content")


class PostAddForm(forms.ModelForm):
    user = forms.CharField(
        label="E-mail",
        disabled=True,
        widget=forms.TextInput(
            attrs={
                "placeholder": "E-mail",
                "required": True,
            }))

    class Meta:
        model = Post
        fields = ("user", "title", "photo", "content")


class ReportAddForm(forms.ModelForm):
    user = forms.CharField(
        label="E-mail",
        disabled=True,
        widget=forms.TextInput(
            attrs={
                "placeholder": "E-mail",
                "required": True,
            }))

    class Meta:
        model = Report
        fields = ("user", "title", "category", "photo", "content", "password")


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
