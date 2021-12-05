# Generated by Django 3.2.9 on 2021-12-05 19:28

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import tinymce.models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('home', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tag_name', models.CharField(max_length=50)),
                ('slug', models.SlugField(unique=True)),
            ],
        ),
        migrations.AddField(
            model_name='group',
            name='name_en',
            field=models.CharField(max_length=128, null=True),
        ),
        migrations.AddField(
            model_name='group',
            name='name_ru',
            field=models.CharField(max_length=128, null=True),
        ),
        migrations.AddField(
            model_name='group',
            name='slug',
            field=models.SlugField(default=uuid.uuid1, unique=True),
        ),
        migrations.AddField(
            model_name='publication',
            name='content_en',
            field=tinymce.models.HTMLField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='publication',
            name='content_ru',
            field=tinymce.models.HTMLField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='publication',
            name='images',
            field=models.ImageField(blank=True, null=True, upload_to='media/'),
        ),
        migrations.AddField(
            model_name='publication',
            name='liked',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='publication',
            name='rating',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='publication',
            name='title_en',
            field=models.CharField(max_length=256, null=True),
        ),
        migrations.AddField(
            model_name='publication',
            name='title_ru',
            field=models.CharField(max_length=256, null=True),
        ),
        migrations.AlterField(
            model_name='publication',
            name='author',
            field=models.ForeignKey(default='creator', on_delete=django.db.models.deletion.PROTECT, related_name='my_publications', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='publication',
            name='content',
            field=tinymce.models.HTMLField(blank=True, null=True),
        ),
        migrations.CreateModel(
            name='Like',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.BooleanField(default=False)),
                ('publication', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.publication')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('published', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('comment', models.TextField(max_length=3000)),
                ('publication', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.publication')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='publication',
            name='tags',
            field=models.ManyToManyField(blank=True, related_name='publications', to='home.Tag'),
        ),
        migrations.CreateModel(
            name='Rate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rate', models.SmallIntegerField(choices=[(1, 'Very bad'), (2, 'Bad'), (3, 'Not bad'), (4, 'Good'), (5, 'Amazing')], default=0)),
                ('publication', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.publication')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('user', 'publication')},
            },
        ),
    ]
