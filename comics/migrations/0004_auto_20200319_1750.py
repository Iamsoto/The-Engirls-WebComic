# Generated by Django 3.0.2 on 2020-03-19 17:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('comics', '0003_comicpanel_youtube_url'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comicpanel',
            name='chapter',
            field=models.FloatField(null=True),
        ),
        migrations.AlterField(
            model_name='comicpanel',
            name='page',
            field=models.IntegerField(null=True),
        ),
    ]
