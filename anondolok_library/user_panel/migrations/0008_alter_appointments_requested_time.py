# Generated by Django 3.2.1 on 2021-07-08 10:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_panel', '0007_alter_appointments_requested_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appointments',
            name='requested_time',
            field=models.TimeField(blank=True, null=True),
        ),
    ]