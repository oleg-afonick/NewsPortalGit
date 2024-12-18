from .models import Post, Category, Comment
from modeltranslation.translator import register, TranslationOptions


@register(Post)
class PostTranslationOptions(TranslationOptions):
    fields = ('post_title', 'post_text',)


@register(Category)
class CategoryTranslationOptions(TranslationOptions):
    fields = ('category_name',)


@register(Comment)
class CommentTranslationOptions(TranslationOptions):
    fields = ('comment_text',)
