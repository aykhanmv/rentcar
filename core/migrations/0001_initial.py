# Generated by Django 4.1.7 on 2023-03-29 07:01

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Car',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time', models.IntegerField(blank=True, null=True)),
                ('about', models.TextField(blank=True, max_length=355, null=True)),
                ('shortAbout', models.CharField(blank=True, max_length=70, null=True)),
                ('marka', models.CharField(blank=True, default='Mercedes', max_length=50, null=True)),
                ('model', models.CharField(blank=True, max_length=70, null=True)),
                ('topSpeed', models.IntegerField(blank=True, null=True)),
                ('nm', models.IntegerField(blank=True, null=True)),
                ('hp', models.IntegerField(blank=True, null=True)),
                ('seats', models.IntegerField(blank=True, null=True)),
                ('price', models.CharField(blank=True, max_length=10, null=True)),
                ('insurance', models.IntegerField(blank=True, null=True)),
                ('tank', models.IntegerField(blank=True, null=True)),
                ('is_booked', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('booker', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='booked_cars', to=settings.AUTH_USER_MODEL)),
                ('company', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='cars', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Year',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=4, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('email', models.EmailField(max_length=40)),
                ('phone', models.CharField(max_length=20)),
                ('message', models.TextField()),
                ('car', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='car_contacts', to='core.car')),
            ],
            options={
                'verbose_name': 'Contact',
                'verbose_name_plural': 'Contacts',
            },
        ),
        migrations.CreateModel(
            name='CarImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(blank=True, null=True, upload_to='images/')),
                ('is_main', models.BooleanField(default=False, help_text='Daxil etdiyiniz şəkillərdən yalnız birini məhsulun əsas şəkli olaraq seçin', verbose_name='Main picture')),
                ('car', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='car_images', to='core.car')),
            ],
            options={
                'verbose_name': 'Car image',
                'verbose_name_plural': 'Car images',
            },
        ),
        migrations.AddField(
            model_name='car',
            name='year_id',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='core.year'),
        ),
    ]
