from django.db import models
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField
from django.shortcuts import reverse


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


class Tag(models.Model):
    tag_name = models.CharField(max_length=50)
    slug = models.SlugField(max_length=50, unique=True)

    def get_absolute_url(self):
        return reverse('tag_detail_url', kwargs={'slug': self.slug})

    def __str__(self):
        return '{}'.format(self.tag_name)


class Publication(models.Model):
    title = models.CharField(max_length=256)
    group = models.ForeignKey(Group, on_delete=models.PROTECT)
    content = RichTextField(null=True, blank=True,)
    author = models.ForeignKey(User, on_delete=models.PROTECT, default='creator', related_name='my_publications')
    slug = models.SlugField(max_length=150, unique=True)
    published = models.DateTimeField(auto_now_add=True, db_index=True)
    rating = models.FloatField(default=0)
    tags = models.ManyToManyField(Tag, blank=True, related_name='publications')

    class Meta:
        ordering = ['-published']

    def get_absolute_url(self):
        return reverse('post_detail_url', kwargs={'slug': self.slug})

    def __str__(self):
        return self.title


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    publication = models.ForeignKey(Publication, on_delete=models.CASCADE)
    published = models.DateTimeField(auto_now_add=True, db_index=True)
    comment = models.TextField(max_length=3000)

    def __str__(self):
        return f'{self.user.username}: {self.publication.title}, {self.published}'
