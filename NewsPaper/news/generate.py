from .models import Post, Author


def generate():
    for number in range(1, 31):
        Post.objects.create(
            author=Author.objects.get(users=1),
            type='NW',
            title=f'Заголовок {number}',
            text=f'Публикация {number}'
        )