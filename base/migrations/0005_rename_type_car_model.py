# Generated by Django 4.2.4 on 2023-08-24 07:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0004_alter_rental_start_date'),
    ]

    operations = [
        migrations.RenameField(
            model_name='car',
            old_name='type',
            new_name='model',
        ),
    ]
