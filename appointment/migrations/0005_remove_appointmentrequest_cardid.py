# Generated by Django 3.2.5 on 2021-07-30 06:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('appointment', '0004_auto_20210730_0053'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='appointmentrequest',
            name='cardId',
        ),
    ]