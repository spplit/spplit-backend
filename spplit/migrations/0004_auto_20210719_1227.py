# Generated by Django 3.2 on 2021-07-19 03:27

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('spplit', '0003_auto_20210718_1658'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='mycard',
            name='tag_list',
        ),
        migrations.AddField(
            model_name='mycard',
            name='tag1',
            field=models.CharField(default=1, max_length=20, verbose_name='태그1'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='mycard',
            name='tag2',
            field=models.CharField(default=django.utils.timezone.now, max_length=20, verbose_name='태그2'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='mycard',
            name='tag3',
            field=models.CharField(default=2, max_length=20, verbose_name='태그3'),
            preserve_default=False,
        ),
        migrations.DeleteModel(
            name='Card',
        ),
    ]
