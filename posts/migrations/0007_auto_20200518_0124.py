# Generated by Django 2.2 on 2020-05-17 19:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0006_auto_20200518_0123'),
    ]

    operations = [
        migrations.RenameField(
            model_name='postlike',
            old_name='posts',
            new_name='post',
        ),
    ]
