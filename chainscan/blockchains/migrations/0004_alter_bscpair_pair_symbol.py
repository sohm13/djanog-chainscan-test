# Generated by Django 4.0.6 on 2022-08-08 07:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blockchains', '0003_bscpair_decimals'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bscpair',
            name='pair_symbol',
            field=models.CharField(max_length=12),
        ),
    ]
