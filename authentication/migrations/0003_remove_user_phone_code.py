# Generated by Django 4.0.3 on 2022-03-28 12:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0002_user_phone_code'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='phone_code',
        ),
    ]
