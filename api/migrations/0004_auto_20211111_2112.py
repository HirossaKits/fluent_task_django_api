# Generated by Django 3.0.7 on 2021-11-11 12:12

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_auto_20211109_2310'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='personalsettings',
            name='id',
        ),
        migrations.AlterField(
            model_name='personalsettings',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, related_name='settings_user', serialize=False, to=settings.AUTH_USER_MODEL),
        ),
    ]
