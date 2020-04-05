# Generated by Django 3.0.4 on 2020-04-05 01:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='zcategory',
            name='hierarchy_index',
        ),
        migrations.AddField(
            model_name='zcategory_product',
            name='hierarchy_index',
            field=models.PositiveSmallIntegerField(default=0),
        ),
    ]
