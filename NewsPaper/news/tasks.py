from celery import shared_task
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.views import View

from .models import Post, Category
import datetime
from django.utils import timezone
import time


@shared_task
def send_email_task(pk):
    post = Post.objects.get(pk=pk)
    categories = post.post_category.all()
    title = post.post_title
    subscribers_emails = []
    for category in categories:
        subscribers_users = category.subscribers.all()
        for sub_user in subscribers_users:
            subscribers_emails.append(sub_user.email)
    html_content = render_to_string(
        'post_created_email.html',
        {
            'text': f'{post.post_title}',
            'link': f'{settings.SITE_URL}/news/{pk}',
        }
    )

    msg = EmailMultiAlternatives(
        subject=title,
        body='',
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=subscribers_emails,
    )

    msg.attach_alternative(html_content, 'text/html')
    msg.send()


@shared_task
def weekly_send_email_task():
    today = timezone.now()
    last_week = today - datetime.timedelta(days=100)
    posts = Post.objects.filter(date_creation__gte=last_week)
    categories = set(posts.values_list('post_category__category_name', flat=True))
    subscribers = set(
        Category.objects.filter(category_name__in=categories).values_list('subscribers__email', flat=True))

    html_content = render_to_string(
        'daily_post.html',
        {
            'link': settings.SITE_URL,
            'posts': posts,
        }

    )
    msg = EmailMultiAlternatives(
        subject='Публикации за неделю',
        body='',
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=subscribers,
    )
    msg.attach_alternative(html_content, 'text/html')
    msg.send()


class MyTasks1(View):

    def get(self, request):
        digit.delay()
        printer.delay()

        return HttpResponse('Hello1')


class MyTasks2(View):

    def get(self, request):
        delay_time = timezone.now() + datetime.timedelta(seconds=5)
        digit.apply_async([10], eta=delay_time)
        printer.delay()

        return HttpResponse('Hello2')


@shared_task
def digit(n):
    for i in range(n):
        time.sleep(1)
        print(i + 1)


@shared_task
def printer():
    time.sleep(5)
    print('Hello World!')
