# Generated by Django 4.1.7 on 2023-04-02 15:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='myuser',
            name='profile_picture',
            field=models.ImageField(blank=True, null=True, upload_to='profile_images'),
        ),
    ]
