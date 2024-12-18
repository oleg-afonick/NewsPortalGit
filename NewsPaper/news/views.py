from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from .filters import PostFilter
from .forms import PostForm, CommentForm
from .models import Author, Comment, User
from .tasks import *
from django.utils.translation import gettext as _



def home(request):
    return render(request, 'home.html')


class PostsList(ListView):
    model = Post
    ordering = '-date_creation'
    context_object_name = 'posts'
    paginate_by = 10

    def get_template_names(self):
        if self.request.path == '/news/':
            self.template_name = 'posts.html'
        elif self.request.path == '/news/top/':
            self.template_name = 'top.html'
        return self.template_name

    def get_ordering(self):
        if self.request.path == '/news/':
            self.ordering = '-date_creation'
        elif self.request.path == '/news/top/':
            self.ordering = '-post_rating'
        return self.ordering

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context


class CommentCreate(LoginRequiredMixin, CreateView):
    form_class = CommentForm
    model = Comment
    template_name = 'post.html'
    permission_required = ('news.add_comment',)

    def form_valid(self, form):
        comment = form.save(commit=False)
        comment.user_id = self.request.user.id
        comment.post_id = self.kwargs['pk']
        comment.save()
        return super().form_valid(form)


class PostDetail(DetailView):
    model = Post
    template_name = 'post.html'
    context_object_name = 'post'
    pk_url_kwarg = "pk"

    def post(self, request, *args, **kwargs):
        post = self.get_object()
        form = CommentForm(request.POST)
        if form.is_valid():
            replay = form.save(commit=False)
            replay.post = post
            replay.user = request.user
            replay.save()
            return redirect('post_detail', pk=post.pk)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = self.object
        comments = post.comment_set.all()
        context['form'] = CommentForm()
        context['comments'] = comments
        context['is_post_likes'] = self.request.user in post.post_likes.all()
        context['is_post_dislikes'] = self.request.user in post.post_dislikes.all()

        return context


class PostSearch(ListView):
    model = Post
    template_name = 'post_search.html'
    context_object_name = 'posts'
    ordering = '-date_creation'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        if self.request.GET:
            return self.filterset.qs
        return Post.objects.none()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        context['not_search'] = not self.request.GET
        return context


class PostCreate(PermissionRequiredMixin, CreateView):
    form_class = PostForm
    model = Post
    template_name = 'post_create.html'
    permission_required = ('news.add_post',)
    success_url = reverse_lazy('post_list')

    # def get_form_kwargs(self):
    #     kwargs = super().get_form_kwargs()
    #     kwargs.update({'user': self.request.user})
    #     return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['add_post_type'] = self.get_type()
        return context

    def form_valid(self, form):
        new_post = form.save(commit=False)
        if self.request.method == 'POST':
            if self.request.path == '/news/articles/create/':
                new_post.post_type = 'AR'
            new_post.author = self.request.user.author
        new_post.save()
        # send_email_task.delay(new_post.pk)
        return super().form_valid(form)

    def get_type(self):
        if self.request.path == '/news/create/':
            return _('Adding news')
        return _('Adding article')


class PostUpdate(PermissionRequiredMixin, UpdateView):
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'
    permission_required = ('news.change_post',)

    # def get_form_kwargs(self):
    #     kwargs = super().get_form_kwargs()
    #     kwargs.update({'user': self.request.user})
    #     return kwargs

    def dispatch(self, request, *args, **kwargs):
        post = self.get_object()

        context = {'post_id': post.pk}
        if post.author.user != self.request.user:
            return render(self.request, 'post_lock.html', context=context)
        elif self.request.path == f'/news/{post.pk}/edit/' and post.post_type != 'NW':
            return render(self.request, 'invalid_articles_edit.html', context=context)
        elif self.request.path == f'/news/articles/{post.pk}/edit/' and post.post_type != 'AR':
            return render(self.request, 'invalid_news_edit.html', context=context)
        return super(PostUpdate, self).dispatch(request, *args, **kwargs)


class PostDelete(PermissionRequiredMixin, DeleteView):
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('post_list')
    permission_required = ('news.delete_post',)

    def dispatch(self, request, *args, **kwargs):
        post = self.get_object()
        context = {'post_id': post.pk}
        if post.author.user != self.request.user:
            return render(self.request, 'post_lock.html', context=context)
        elif self.request.path == f'/news/{post.pk}/delete/' and post.post_type != 'NW':
            return render(self.request, 'invalid_articles_delete.html', context=context)
        elif self.request.path == f'/news/articles/{post.pk}/delete/' and post.post_type != 'AR':
            return render(self.request, 'invalid_news_delete.html', context=context)
        return super(PostDelete, self).dispatch(request, *args, **kwargs)


class CategoryListView(ListView):
    model = Post
    template_name = 'category_list.html'
    context_object_name = 'category_posts_list'
    paginate_by = 10

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.post_category = None

    def get_queryset(self):
        self.post_category = get_object_or_404(Category, id=self.kwargs['pk'])
        queryset = Post.objects.filter(post_category=self.post_category).order_by('-date_creation')
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_subscriber'] = self.request.user not in self.post_category.subscribers.all()
        context['is_subscriber'] = self.request.user in self.post_category.subscribers.all()
        context['category'] = self.post_category
        return context


@login_required
def subscribe(request, pk):
    user = request.user
    category = Category.objects.get(id=pk)
    category.subscribers.add(user)
    return redirect('category_list', pk)


@login_required
def unsubscribe(request, pk):
    user = request.user
    category = Category.objects.get(id=pk)
    category.subscribers.remove(user)
    return redirect('category_list', pk)


@login_required
def post_like(request, pk):
    user = request.user
    post = Post.objects.get(id=pk)
    if user not in post.post_likes.all():
        post.post_likes.add(user)
        post.like()
    else:
        post.post_likes.remove(user)
        post.dislike()
    post.author.update_rating()
    return redirect(f'/news/{post.pk}')


@login_required
def post_dislike(request, pk):
    user = request.user
    post = Post.objects.get(id=pk)
    if user not in post.post_dislikes.all():
        post.post_dislikes.add(user)
        post.dislike()
    else:
        post.post_dislikes.remove(user)
        post.like()
    post.author.update_rating()
    return redirect(f'/news/{post.pk}')


@login_required
def comment_like(request, pk):
    user = request.user
    comment = Comment.objects.get(id=pk)
    post = Post.objects.get(id=comment.post_id)
    if user not in comment.comment_likes.all():
        comment.comment_likes.add(user)
        comment.like()
    else:
        comment.comment_likes.remove(user)
        comment.dislike()
    post.author.update_rating()
    return redirect(f'/news/{comment.post_id}')
    # return redirect(f'/news/comment/{comment.pk}/')


@login_required
def comment_dislike(request, pk):
    user = request.user
    comment = Comment.objects.get(id=pk)
    post = Post.objects.get(id=comment.post_id)
    if user not in comment.comment_dislikes.all():
        comment.comment_dislikes.add(user)
        comment.dislike()
    else:
        comment.comment_dislikes.remove(user)
        comment.like()
    post.author.update_rating()
    return redirect(f'/news/{comment.post_id}')
    # return redirect(f'/news/comment/{comment.pk}/')


class AuthorsListView(ListView):
    model = Post
    template_name = 'authors_list.html'
    context_object_name = 'authors_post_list'
    paginate_by = 10

    def get_queryset(self):
        self.author = get_object_or_404(Author, id=self.kwargs['pk'])
        queryset = Post.objects.filter(author=self.author).order_by('-date_creation')
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['author'] = self.author
        return context


class UserCommentListView(ListView):
    model = Comment
    template_name = 'user_comment_list.html'
    context_object_name = 'user_comment_post_list'
    paginate_by = 10

    def get_queryset(self):
        self.user = get_object_or_404(User, id=self.kwargs['pk'])
        queryset = Comment.objects.filter(user=self.user).order_by('-date_creation')
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.user
        return context


class PostTypeListView(ListView):
    model = Post
    template_name = 'post_type.html'
    context_object_name = 'post_type_list'
    paginate_by = 10

    def get_queryset(self):
        queryset = Post.objects.filter(post_type=self.get_type()[0]).order_by('-date_creation')
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['count_post_type'] = self.get_type()[1]
        return context

    def get_type(self):
        if self.request.path == '/news/type/NW/':
            return 'NW', _('Total news')
        return 'AR', _('Total articles')


class CommentsPostListView(ListView):
    model = Comment
    ordering = '-date_creation'
    template_name = 'comments_post_list.html'
    context_object_name = 'comments_post'
    paginate_by = 10

    def get_queryset(self):
        self.post = get_object_or_404(Post, id=self.kwargs['pk'])
        queryset = Comment.objects.filter(post=self.post).order_by('-date_creation')
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['post'] = self.post
        return context


class CommentPostDetail(DetailView):
    model = Comment
    template_name = 'post_comment.html'
    context_object_name = 'comment'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        self.comment = get_object_or_404(Comment, id=self.kwargs['pk'])
        post = Post.objects.get(id=self.comment.post_id)
        context['comment'] = self.comment
        context['post'] = post
        context['is_comment_likes'] = self.request.user in self.comment.comment_likes.all()
        context['is_comment_dislikes'] = self.request.user in self.comment.comment_dislikes.all()
        return context


class CommentUpdate(LoginRequiredMixin, UpdateView):
    form_class = CommentForm
    model = Comment
    template_name = 'comment_edit.html'
    permission_required = ('news.change_comment',)

    def dispatch(self, request, *args, **kwargs):
        comment = self.get_object()
        if comment.user != self.request.user:
            return render(self.request, 'comment_lock.html')
        return super(CommentUpdate, self).dispatch(request, *args, **kwargs)


class CommentDelete(LoginRequiredMixin, DeleteView):
    model = Comment
    template_name = 'comment_delete.html'
    permission_required = ('news.delete_comment',)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        comment = get_object_or_404(Comment, id=self.kwargs['pk'])
        context['post'] = comment.post
        return context

    def dispatch(self, request, *args, **kwargs):
        comment = self.get_object()
        if comment.user != self.request.user:
            return render(self.request, 'comment_lock.html')
        return super(CommentDelete, self).dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('post_comments_list', kwargs={'pk': self.object.post.pk})


def handler403(request, exception, template_name='403.html'):
    return render(request, '403.html')


class CategoryList(ListView):
    model = Category
    template_name = 'categories.html'
    context_object_name = 'categories'


class GetChoices(ListView):
    model = Post
    template_name = 'choices.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        choices = [c[1] for c in Post.SELECT_POST]
        context['choices'] = choices

        return context


def get_session_timezone(request):
    if request.POST:
        request.session['django_timezone'] = request.POST['timezone']
        return redirect(request.META['HTTP_REFERER'])


def post_test(request):
    posts = Post.objects.all()
    context = {"posts": posts}
    if request.method == "POST":
        data = request.POST.get("test")
        data2 = request.POST.get("test2")
        return render(request, "post_test.html", {"posts": posts, "data": data, "data2": data2})
    return render(request, "post_test.html", context)
