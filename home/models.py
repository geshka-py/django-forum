from django.db import models
from django.contrib.auth.models import User


class Group(models.Model):
    name = models.CharField(max_length=128)

    def __str__(self):
        return self.name


class Publication(models.Model):
    title = models.CharField(max_length=256)
    group = models.ForeignKey(Group, on_delete=models.PROTECT)
    content = models.TextField(null=True, blank=True,)
    author = models.ForeignKey(User, on_delete=models.PROTECT, default='creator', related_name='my_publications')
    published = models.DateTimeField(auto_now_add=True, db_index=True)
    readers = models.ManyToManyField(User, through='UserPublicationRelation',  related_name='publications')

    class Meta:
        ordering = ['-published']

    def __str__(self):
        return self.title


class UserPublicationRelation(models.Model):
    RATE_CHOICES = (
        (1, 'Very bad'),
        (2, 'Bad'),
        (3, 'Not bad'),
        (4, 'Good'),
        (5, 'Amazing'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    publication = models.ForeignKey(Publication, on_delete=models.CASCADE)
    rate = models.PositiveSmallIntegerField(choices=RATE_CHOICES, null=True)
    comment = models.TextField(max_length=3000, blank=True)
    published = models.DateTimeField(auto_now_add=True, db_index=True)
    like = models.BooleanField(default=False)

    class Meta:
        ordering = ['-published']

    def __str__(self):
        return f'{self.user.username}: {self.publication.title}, RATE: {self.rate}'
