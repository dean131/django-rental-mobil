# Generated by Django 4.2.4 on 2023-09-03 22:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0002_alter_car_price_alter_rental_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='car',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='car',
            name='name',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='car',
            name='passenger_capacity',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='car',
            name='price',
            field=models.IntegerField(null=True),
        ),
    ]