# Generated by Django 5.0 on 2024-01-05 10:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Ai_reader', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='chat',
            name='active',
            field=models.BooleanField(default=False),
        ),
    ]
