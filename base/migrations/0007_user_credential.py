# Generated by Django 4.1 on 2022-09-09 12:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0006_remove_upvotepost_post_remove_upvotepost_user_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='credential',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
