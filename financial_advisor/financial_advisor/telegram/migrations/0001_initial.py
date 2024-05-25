# Generated by Django 4.2.13 on 2024-05-25 11:44

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='TelegramMessage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('chat_id', models.CharField(max_length=255)),
                ('message_id', models.CharField(max_length=255)),
                ('text', models.TextField()),
                ('date', models.DateTimeField()),
            ],
        ),
    ]
