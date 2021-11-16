from django.db import models
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField


class Group(models.Model):
    name = models.CharField(max_length=128)

    def __str__(self):
        return self.name


class Rate(models.Model):
    RATE_CHOICES = (
        (1, 'Very bad'),
        (2, 'Bad'),
        (3, 'Not bad'),
        (4, 'Good'),
        (5, 'Amazing'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    publication = models.ForeignKey('Publication', on_delete=models.CASCADE)
    rate = models.SmallIntegerField(choices=RATE_CHOICES, default=0)

    class Meta:
        unique_together = ('user', 'publication')

    def __str__(self):
        return f'{self.user.username}: {self.publication.title}, RATE: {self.rate}'


class Publication(models.Model):
    title = models.CharField(max_length=256)
    group = models.ForeignKey(Group, on_delete=models.PROTECT)
    description = models.CharField(max_length=512, null=True)
    content = RichTextField(null=True, blank=True,)
    author = models.ForeignKey(User, on_delete=models.PROTECT, default='creator', related_name='my_publications')
    published = models.DateTimeField(auto_now_add=True, db_index=True)
    rating = models.FloatField(default=0)

    class Meta:
        ordering = ['-published']

    def __str__(self):
        return self.title


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    publication = models.ForeignKey(Publication, on_delete=models.CASCADE)
    published = models.DateTimeField(auto_now_add=True, db_index=True)
    comment = models.TextField(max_length=3000)

    def __str__(self):
        return f'{self.user.username}: {self.publication.title}, {self.published}'
