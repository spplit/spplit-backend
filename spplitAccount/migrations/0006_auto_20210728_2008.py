# Generated by Django 3.2.5 on 2021-07-28 11:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('spplitAccount', '0005_auto_20210728_1826'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='category3',
            field=models.CharField(default='Work', max_length=30),
        ),
        migrations.AlterField(
            model_name='category',
            name='category4',
            field=models.CharField(default='Teams', max_length=30),
        ),
        migrations.AlterField(
            model_name='user',
            name='category3',
            field=models.CharField(default='Work', max_length=30),
        ),
        migrations.AlterField(
            model_name='user',
            name='category4',
            field=models.CharField(default='Teams', max_length=30),
        ),
    ]
