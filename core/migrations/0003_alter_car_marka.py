# Generated by Django 4.1.7 on 2023-04-02 15:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_alter_car_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='car',
            name='marka',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
