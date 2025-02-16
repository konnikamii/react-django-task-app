# Generated by Django 5.1.5 on 2025-01-18 23:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_rename_owned_id_task_owner_id'),
    ]

    operations = [
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('email', models.EmailField(max_length=200)),
                ('subject', models.CharField(max_length=200)),
                ('message', models.TextField(max_length=1500)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
