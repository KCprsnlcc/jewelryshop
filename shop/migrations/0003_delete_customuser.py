# Generated by Django 5.1 on 2024-08-17 14:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0002_customuser'),
    ]

    operations = [
        migrations.DeleteModel(
            name='CustomUser',
        ),
    ]
