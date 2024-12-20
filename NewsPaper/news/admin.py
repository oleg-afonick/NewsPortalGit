from django.contrib import admin
from .models import *
from modeltranslation.admin import TranslationAdmin


class CategoryInline(admin.TabularInline):
    model = PostCategory
    extra = 1


class PostAdmin(admin.ModelAdmin):
    model = Post
    inlines = (CategoryInline,)
    list_display = ('id', 'post_title', 'preview', 'date_creation', 'category', 'post_rating', 'likes', 'dislikes',)
    list_display_links = ('post_title',)
    list_filter = ('author', 'post_category', 'date_creation',)
    search_fields = ('post_title', 'post_text', 'author__user__username', 'post_rating')

    def preview(self, obj):
        return obj.preview

    def category(self, obj):
        return ", ".join([category.category_name for category in obj.post_category.all()])

    def likes(self, obj):
        return ", ".join([user.username for user in obj.post_likes.all()])

    def dislikes(self, obj):
        return ", ".join([user.username for user in obj.post_dislikes.all()])

    preview.short_description = 'Содержание'
    category.short_description = 'Категории'
    likes.short_description = 'Нравится'
    dislikes.short_description = 'Не нравится'


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'category_name',)
    list_display_links = ('category_name',)


class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'comment_text', 'user', 'date_creation', 'comment_rating', 'post')
    list_display_links = ('comment_text',)
    list_filter = ('user', 'post',)


class AuthorAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'author_rating')
    list_display_links = ('user',)


class TransPostAdmin(PostAdmin, TranslationAdmin):
    model = Post


class TransCategoryAdmin(CategoryAdmin, TranslationAdmin):
    model = Category


class TransCommentAdmin(CommentAdmin, TranslationAdmin):
    model = Comment


admin.site.register(Post, TransPostAdmin)
admin.site.register(Category, TransCategoryAdmin)
admin.site.register(Comment, TransCommentAdmin)
admin.site.register(Author, AuthorAdmin)
