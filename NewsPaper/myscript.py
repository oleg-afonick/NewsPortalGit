from news.models import *

print()
print('Список авторов:')
authors = Author.objects.values('id', 'user__username')

for author in authors:
    id = author['id']
    username = author['user__username']
    print(f'{id}. {username}')

print()
print('Список категорий:')
categories = Category.objects.values('id', 'category_name')

for category in categories:
    id = category['id']
    name = category['category_name']
    print(f'{id}. {name}')


# echo 'import myscript' | python manage.py shell
# exec(open('myscript.py',  encoding="utf-8").read())
