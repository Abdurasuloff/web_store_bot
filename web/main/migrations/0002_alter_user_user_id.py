# Generated by Django 5.0.1 on 2024-01-25 06:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='user_id',
            field=models.PositiveBigIntegerField(unique=True),
        ),
    ]
