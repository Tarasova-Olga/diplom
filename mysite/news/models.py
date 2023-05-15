from django.db import models

class Articles(models.Model):                      # создали табличку с 3-мя полями (заголовок, сам пост, дата)
    title = models.CharField(max_length=120)
    post = models.TextField()
    date = models.DateTimeField()

    def __str__(self):
        return self.title            # обращаясь к title будет выдать сами заголовки, а не их объекты
