# Generated by Django 3.2.9 on 2021-11-10 15:17

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('home', '0005_auto_20211110_1706'),
    ]

    operations = [
        migrations.AddField(
            model_name='publication',
            name='readers',
            field=models.ManyToManyField(related_name='publications', through='home.UserPublicationRelation', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='publication',
            name='author',
            field=models.ForeignKey(default='creator', on_delete=django.db.models.deletion.PROTECT, related_name='my_publications', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='userpublicationrelation',
            name='comment',
            field=models.TextField(blank=True, max_length=3000),
        ),
    ]