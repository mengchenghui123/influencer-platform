# Generated by Django 3.2.25 on 2024-11-25 22:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_auto_20241122_1751'),
    ]

    operations = [
        migrations.RenameField(
            model_name='customuser',
            old_name='avatar',
            new_name='avatarFile',
        ),
    ]
