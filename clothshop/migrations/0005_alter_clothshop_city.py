# Generated by Django 4.0.3 on 2022-03-28 12:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0003_remove_user_phone_code'),
        ('clothshop', '0004_remove_clothshop_disabled'),
    ]

    operations = [
        migrations.AlterField(
            model_name='clothshop',
            name='city',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='cloth_shops', to='authentication.city', verbose_name='city'),
        ),
    ]
