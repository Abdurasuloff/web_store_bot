# Generated by Django 5.0.1 on 2024-02-06 11:45

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0010_alter_user_total_price'),
    ]

    operations = [
        migrations.CreateModel(
            name='History',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('status', models.CharField(choices=[('Tayyorlanmoqda', 'preparing'), ('Yetkazilmoqd', 'delivering'), ('Yetkazib berildi', 'finished')], max_length=50)),
                ('products', models.ManyToManyField(to='main.product')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.user')),
            ],
        ),
    ]
