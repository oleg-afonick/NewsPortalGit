from django.urls import path
from .views import *

from django.views.decorators.cache import cache_page

urlpatterns = [
    path('', PostsList.as_view(), name='post_list'),
    path('<int:pk>/', PostDetail.as_view(), name='post_detail'),
    path('search/', PostSearch.as_view(), name='post_search'),
    path('create/', PostCreate.as_view(), name='post_create'),
    path('<int:pk>/edit/', PostUpdate.as_view(), name='post_edit'),
    path('<int:pk>/delete/', PostDelete.as_view(), name='post_delete'),
    path('articles/create/', PostCreate.as_view(), name='articles_create'),
    path('articles/<int:pk>/edit/', PostUpdate.as_view(), name='articles_edit'),
    path('articles/<int:pk>/delete/', PostDelete.as_view(), name='articles_delete'),
    path('categories/<int:pk>/', CategoryListView.as_view(), name='category_list'),
    path('categories/<int:pk>/subscribe/', subscribe, name='subscribe'),
    path('categories/<int:pk>/unsubscribe/', unsubscribe, name='unsubscribe'),
    path('author/<int:pk>/', AuthorsListView.as_view(), name='author_list'),
    path('type/<str:post_type>/', PostTypeListView.as_view(), name='type_list'),
    path('comments/user/<int:pk>/', UserCommentListView.as_view(), name='user_comments_list'),
    path('<int:pk>/comments/', CommentsPostListView.as_view(), name='post_comments_list'),
    path('comment/<int:pk>/', CommentPostDetail.as_view(), name='post_comment_detail'),
    path('<int:pk>/comment/create/', CommentCreate.as_view(), name='comment_create'),
    path('<int:pk>/like/', post_like, name='post_like'),
    path('<int:pk>/dislike/', post_dislike, name='post_dislike'),
    path('comment/<int:pk>/like/', comment_like, name='comment_like'),
    path('comment/<int:pk>/dislike/', comment_dislike, name='comment_dislike'),
    path('comment/<int:pk>/edit/', CommentUpdate.as_view(), name='comment_edit'),
    path('comment/<int:pk>/delete/', CommentDelete.as_view(), name='comment_delete'),
    path('top/', PostsList.as_view(), name='top_list'),
    path('categories/', CategoryList.as_view(), name='categories'),
    path('choices/', cache_page(60 * 5)(GetChoices.as_view()), name='get_choices'),
    path('task/', MyTasks1.as_view()),
    path('post_test/', post_test),
]
