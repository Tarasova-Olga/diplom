from django.http import Http404
from django.shortcuts import render
from .models import Post


def view_post(request, slug):
    try:
        post = Post.objects.get(slug=slug)

    except Post.DoesNotExist:
        raise Http404("Пост не существует. Выдохните и вернитесь на главную =)")

    return render(request, 'publisher/post.html', context={'post': post})
