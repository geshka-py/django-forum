from django.db import models


class VoteButton(models.Model):
    name = models.CharField(max_length=256)
    count = models.IntegerField(default=0)

    def __str__(self):
        return self.name


class Message(models.Model):
    message = models.CharField(max_length=256, default=None)
    btn = models.ForeignKey(VoteButton, on_delete=models.CASCADE)

    def __str__(self):
        return self.message
