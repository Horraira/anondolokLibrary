# Generated by Django 3.2.1 on 2021-08-08 07:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admin_panel', '0016_wish_list'),
    ]

    operations = [
        migrations.AddField(
            model_name='wish_list',
            name='is_wished',
            field=models.BooleanField(default=False),
        ),
    ]
