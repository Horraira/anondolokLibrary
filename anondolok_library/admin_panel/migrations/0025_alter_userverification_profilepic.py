# Generated by Django 3.2.1 on 2021-08-19 15:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admin_panel', '0024_alter_userverification_profilepic'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userverification',
            name='profilePic',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
    ]
