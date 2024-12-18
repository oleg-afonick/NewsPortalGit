from django import forms
from django.core.exceptions import ValidationError

from NewsPaper.settings import logger
from .models import Post, Comment
from django.utils.translation import gettext_lazy as _
import logging


class PostForm(forms.ModelForm):

    # def __init__(self, *args, **kwargs):
    #     self.user = kwargs.pop('user')
    #     super().__init__(*args, **kwargs)

        # if not self.user.is_superuser:
        #     self.fields.pop('post_title')

    class Meta:
        model = Post
        fields = ['post_title', 'post_text', 'post_category']
        labels = {
            'post_title': _('Header'),
            'post_text': _('Content'),
            'post_category': _('Categories'),
        }
        widgets = {
            'post_title': forms.Textarea(attrs={'class': 'form-text', 'cols': 70, 'rows': 3}),
            'post_text': forms.Textarea(attrs={'class': 'form-text', 'cols': 70, 'rows': 10}),
        }

    def clean(self):
        cleaned_data = super().clean()
        post_title = cleaned_data.get('post_title')
        post_text = cleaned_data.get('post_text')
        if post_text is not None and post_text == post_title:
            logger.warning('Текст статьи не должен совпадать с заголовком')
            raise ValidationError({
                'post_text': _('The text of the article should not match the title')
            })

        return cleaned_data


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['comment_text']
        labels = {
            'comment_text': _('Enter comment text'),
        }
        widgets = {
            'comment_text': forms.Textarea(attrs={'class': 'form-text', 'cols': 200, 'rows': 2}),
        }
