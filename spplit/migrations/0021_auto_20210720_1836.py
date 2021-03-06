# Generated by Django 3.2 on 2021-07-20 09:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('spplit', '0020_rename_follow_card_id_relation_follow_card'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='card',
            name='email',
        ),
        migrations.RemoveField(
            model_name='card',
            name='job',
        ),
        migrations.RemoveField(
            model_name='card',
            name='phone',
        ),
        migrations.RemoveField(
            model_name='card',
            name='tag1',
        ),
        migrations.RemoveField(
            model_name='card',
            name='tag2',
        ),
        migrations.RemoveField(
            model_name='card',
            name='tag3',
        ),
        migrations.RemoveField(
            model_name='card',
            name='unique_num',
        ),
        migrations.AddField(
            model_name='card',
            name='follow_mycard',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='spplit.mycard'),
            preserve_default=False,
        ),
    ]
