# Generated by Django 5.0.1 on 2024-02-01 12:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0008_user_products_user_total_price_delete_cart'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='user_id',
        ),
        migrations.AlterField(
            model_name='user',
            name='id',
            field=models.PositiveBigIntegerField(primary_key=True, serialize=False, unique=True),
        ),
    ]