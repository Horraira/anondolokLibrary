# Generated by Django 3.2.4 on 2021-06-16 04:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('login_signup', '0005_rename_user_demo_user'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='demo_user',
            new_name='user',
        ),
    ]
