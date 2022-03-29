# Generated by Django 4.0.3 on 2022-03-29 16:13

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('shops', '0005_tailorshop_delivery_location'),
    ]

    operations = [
        migrations.CreateModel(
            name='ShopDevice',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('device_id', models.CharField(max_length=500, verbose_name='device_id')),
                ('device_type', models.CharField(choices=[('M', 'Mobile'), ('T', 'Tablet')], default='M', max_length=50, verbose_name='device_type')),
                ('manufaturer', models.CharField(max_length=255, null=True, verbose_name='manufaturer')),
                ('device_name', models.CharField(max_length=255, verbose_name='device_name')),
                ('Device_Model', models.CharField(max_length=255, verbose_name='Device_Model')),
                ('OS_Type', models.CharField(choices=[('A', 'Android'), ('IP', 'Iphone')], default='A', max_length=50, verbose_name='OS_Type')),
                ('OS_ID', models.CharField(max_length=255, null=True, verbose_name='OS_ID')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='user')),
            ],
        ),
    ]
