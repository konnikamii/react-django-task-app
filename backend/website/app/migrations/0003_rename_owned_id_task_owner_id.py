# Generated by Django 5.1.4 on 2025-01-13 19:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_rename_user_task_owned_id'),
    ]

    operations = [
        migrations.RenameField(
            model_name='task',
            old_name='owned_id',
            new_name='owner_id',
        ),
    ]
