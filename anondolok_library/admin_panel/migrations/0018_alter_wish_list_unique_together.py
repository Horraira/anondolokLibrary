# Generated by Django 3.2.1 on 2021-08-08 07:24

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('admin_panel', '0017_wish_list_is_wished'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='wish_list',
            unique_together={('user', 'book')},
        ),
    ]