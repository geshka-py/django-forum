# Generated by Django 3.2.9 on 2021-11-18 09:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0015_auto_20211116_1545'),
    ]

    operations = [
        migrations.AlterField(
            model_name='publication',
            name='tags',
            field=models.ManyToManyField(blank=True, db_table='app_propertytype_itemtypes', related_name='publications', to='home.Tag'),
        ),
    ]
