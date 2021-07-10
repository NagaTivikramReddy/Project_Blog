from django.forms import fields
from blogs.models import User
from django import forms
from blogs.models import Post, Comment


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ("title", "text")

        widgets = {
            "title": forms.TextInput(attrs={"class": " textinputclass"}),
            "text": forms.Textarea(
                attrs={"class": "editable medium-editor-textarea postcontent"}
            ),
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ("text",)

        widgets = {
            # "author": forms.TextInput(attrs={"class": "textinputclass"}),
            "text": forms.Textarea(attrs={"class": "editable medium-editor"}),
        }



