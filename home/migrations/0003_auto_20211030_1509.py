# Generated by Django 3.2.8 on 2021-10-30 12:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0002_votebutton_messages'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='votebutton',
            name='messages',
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.CharField(default=None, max_length=256)),
                ('btn', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.votebutton')),
            ],
        ),
    ]
