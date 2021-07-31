# Generated by Django 3.2.5 on 2021-07-29 14:30

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('appointment', '0002_auto_20210729_2318'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appointmentrequest',
            name='receiver',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='appointment_receiver', to=settings.AUTH_USER_MODEL),
        ),
    ]
