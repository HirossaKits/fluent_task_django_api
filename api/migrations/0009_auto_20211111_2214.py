# Generated by Django 3.0.7 on 2021-11-11 13:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0008_personalsettings_project'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='PersonalSettings',
            new_name='PersonalSetting',
        ),
    ]
