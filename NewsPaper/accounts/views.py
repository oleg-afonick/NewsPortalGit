from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User, Group
from django.shortcuts import redirect, render
from django.views.generic import TemplateView, CreateView, DetailView, UpdateView, DeleteView
from accounts.forms import BaseRegisterForm, UserForm
from news.models import Author


class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_author'] = not self.request.user.groups.filter(name='authors').exists()
        context['is_author'] = self.request.user.groups.filter(name='authors').exists()
        return context


class ProfileDetail(LoginRequiredMixin, DetailView):
    model = User
    template_name = 'profile_detail.html'
    context_object_name = 'user'

    def get_context_data(self, **kwargs):
        user = self.get_object()
        context = super().get_context_data(**kwargs)
        context['is_not_author'] = not user.groups.filter(name='authors').exists()
        context['is_author'] = user.groups.filter(name='authors').exists()
        return context


class ProfileUpdate(LoginRequiredMixin, UpdateView):
    model = User
    template_name = 'profile_update.html'
    form_class = UserForm
    context_object_name = 'user'
    success_url = '/accounts/profile/'

    def dispatch(self, request, *args, **kwargs):
        user = self.get_object()
        if user != self.request.user:
            return render(self.request, 'profile_lock.html')
        return super(ProfileUpdate, self).dispatch(request, *args, **kwargs)


class ProfileDelete(LoginRequiredMixin, DeleteView):
    template_name = 'profile_delete.html'
    queryset = User.objects.all()
    success_url = '/'

    def dispatch(self, request, *args, **kwargs):
        user = self.get_object()
        if user != self.request.user:
            return render(self.request, '403.html')
        return super(ProfileDelete, self).dispatch(request, *args, **kwargs)


class BaseRegisterView(CreateView):
    model = User
    form_class = BaseRegisterForm
    success_url = '/login/'


@login_required
def upgrade_me(request):
    user = request.user
    authors_group = Group.objects.get(name='authors')
    if not request.user.groups.filter(name='authors').exists():
        authors_group.user_set.add(user)
    Author.objects.create(user=user)
    return redirect('/author_now/')


@login_required
def author_now(request):
    if not request.user.groups.filter(name='authors').exists():
        return redirect('/profile/')
    return render(request, 'author_now.html')
