# Generated by Django 3.2.1 on 2021-07-08 10:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_panel', '0003_alter_appointments_check_approve'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appointments',
            name='requested_time',
            field=models.CharField(max_length=50, null=True),
        ),
    ]
