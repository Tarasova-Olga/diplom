from django.urls import path
from django.conf.urls import include
from django.views.generic import ListView, DetailView
from .models import Articles   #импортируем нашу табличку, чтобы из нее вытягивать данные


urlpatterns = [
    path('', ListView.as_view(queryset=Articles.objects.all().order_by("-date")[:20],           #выводим срез 20 постов, по дате (- сразу новые)
                              template_name="news/posts.html")),
    path('<int:pk>/', DetailView.as_view(model=Articles, template_name="news/post.html"))
]