# Generated by Django 3.1.5 on 2021-02-01 18:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ecom', '0008_remove_user_mobile_no'),
    ]

    operations = [
        migrations.AddField(
            model_name='cart',
            name='color',
            field=models.CharField(default='red', max_length=255),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='order_item',
            name='color',
            field=models.CharField(default='red', max_length=255),
            preserve_default=False,
        ),
    ]
