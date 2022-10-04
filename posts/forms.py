from django import forms
from posts.models import POST_TYPE_CHOICES
from posts.models import Post


class PostForm(forms.Form):
    title = forms.CharField(
        label="",
        max_length=95,
        min_length=8,
    )
    description = forms.CharField(
        widget=forms.Textarea()
    )
    stars = forms.IntegerField(max_value=5, min_value=0)
    type = forms.ChoiceField(choices=POST_TYPE_CHOICES)


class CommentForm(forms.Form):
    author = forms.CharField(
        label="",
        max_length=95,
        min_length=8,
    )
    text = forms.CharField(
        widget=forms.Textarea()
    )
