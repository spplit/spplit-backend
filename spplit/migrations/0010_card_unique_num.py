# Generated by Django 3.2 on 2021-07-19 06:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('spplit', '0009_auto_20210719_1458'),
    ]

    operations = [
        migrations.AddField(
            model_name='card',
            name='unique_num',
            field=models.CharField(default=0, max_length=100, verbose_name='고유번호'),
        ),
    ]
