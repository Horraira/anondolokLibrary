# Generated by Django 3.2.4 on 2021-06-27 11:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admin_panel', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='books',
            name='book_pages',
            field=models.BigIntegerField(null=True),
        ),
        migrations.AddField(
            model_name='books',
            name='publisher_date',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='books',
            name='quantity',
            field=models.BigIntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='books',
            name='description',
            field=models.TextField(max_length=500, null=True),
        ),
        migrations.AlterField(
            model_name='books',
            name='shelf_number',
            field=models.CharField(max_length=20, null=True),
        ),
    ]
