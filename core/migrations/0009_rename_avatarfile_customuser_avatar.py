# Generated by Django 3.2.25 on 2024-11-25 22:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0008_rename_avatar_customuser_avatarfile'),
    ]

    operations = [
        migrations.RenameField(
            model_name='customuser',
            old_name='avatarFile',
            new_name='avatar',
        ),
    ]