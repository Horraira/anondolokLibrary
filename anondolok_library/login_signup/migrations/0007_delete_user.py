# Generated by Django 3.2.4 on 2021-06-16 11:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('login_signup', '0006_rename_demo_user_user'),
    ]

    operations = [
        migrations.DeleteModel(
            name='user',
        ),
    ]
