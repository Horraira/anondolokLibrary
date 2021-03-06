# Generated by Django 3.2.4 on 2021-06-27 08:44

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Books',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('book_name', models.CharField(max_length=200, null=True)),
                ('author_name', models.CharField(max_length=200, null=True)),
                ('category', models.CharField(max_length=200, null=True)),
                ('isbn_number', models.CharField(max_length=20)),
                ('doi_number', models.CharField(max_length=100)),
                ('publisher_name', models.CharField(max_length=200)),
                ('shelf_number', models.CharField(max_length=20)),
                ('description', models.TextField(max_length=500)),
            ],
        ),
    ]
