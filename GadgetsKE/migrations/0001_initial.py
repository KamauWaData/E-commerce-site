# Generated by Django 5.1.3 on 2025-01-06 12:14

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='products',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('discount', models.FloatField()),
                ('composition', models.TextField(default='')),
                ('prodapp', models.TextField(default='')),
                ('category', models.CharField(choices=[('CZ', 'Cheese'), ('ML', 'Milk'), ('CR', 'Curd'), ('LS', 'Lassi'), ('PN', 'Paneer'), ('MS', 'Milkshake'), ('IC', 'Ice-Creams'), ('GH', 'Ghee')], max_length=2)),
                ('image', models.ImageField(upload_to='product')),
            ],
        ),
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('locality', models.CharField(max_length=200)),
                ('city', models.CharField(max_length=50)),
                ('mobile', models.IntegerField(default=0)),
                ('zipcode', models.IntegerField()),
                ('state', models.CharField(choices=[('KMB', 'Kiambu'), ('NRB', 'Nairobi'), ('MSA', 'Mombasa'), ('TVT', 'Taita Taveta'), ('KLF', 'Kilifi'), ('LMU', 'Lamu'), ('KSI', 'Kisii'), ('ELD', 'Eldoret'), ('KRC', 'Kericho'), ('KSM', 'Kisumu'), ('HMB', 'Homa Bay'), ('MCK', 'Machakos'), ('MK', 'Makueni'), ('KJD', 'Kajiado'), ('NRK', 'Narok'), ('MRSB', 'Marsabit'), ('TRK', 'Turkana'), ('MDR', 'Mandera')], max_length=100)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveBigIntegerField(default=1)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='GadgetsKE.products')),
            ],
        ),
    ]
