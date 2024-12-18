from django_filters import FilterSet, DateFilter, CharFilter, ModelChoiceFilter, ChoiceFilter, NumberFilter
from .models import Author, Category, Post
from django import forms
from django.utils.translation import gettext_lazy as _


class PostFilter(FilterSet):
    search_title = CharFilter(
        field_name='post_title',
        label=_('Header contains'),
        lookup_expr='iregex'
    )

    search_text = CharFilter(
        field_name='post_text',
        label=_('Text contains'),
        lookup_expr='iregex'
    )

    search_rating = NumberFilter(
        field_name='post_rating',
        label=_('Rating'),
        lookup_expr='exact'
    )

    search_author = ModelChoiceFilter(
        empty_label=_('All authors'),
        field_name='author',
        label=_('Author'),
        queryset=Author.objects.all()
    )

    search_category = ModelChoiceFilter(
        empty_label=_('All categories'),
        field_name='post_category',
        label=_('Category'),
        queryset=Category.objects.all()
    )

    search_type = ChoiceFilter(
        empty_label=_('All types'),
        field_name='post_type',
        label=_('Type'),
        choices=Post.SELECT_POST
    )

    post_date = DateFilter(
        field_name='date_creation',
        widget=forms.DateInput(attrs={'type': 'date'}),
        label=_('Date'),
        lookup_expr='date__gte',
    )
