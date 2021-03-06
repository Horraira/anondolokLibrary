# Generated by Django 3.2.1 on 2021-08-26 06:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admin_panel', '0027_alter_userverification_profilepic'),
    ]

    operations = [
        migrations.AlterField(
            model_name='books',
            name='cover_photo',
            field=models.ImageField(blank=True, null=True, upload_to='bookCoverPhotos'),
        ),
        migrations.AlterField(
            model_name='userverification',
            name='profilePic',
            field=models.ImageField(blank=True, default='profile.png', null=True, upload_to='profilePic'),
        ),
    ]
