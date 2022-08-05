# Generated by Django 4.0.6 on 2022-07-08 12:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('blockchains', '0002_rename_bsc_bsctransaction_alter_bsctransaction_table'),
    ]

    operations = [
        migrations.CreateModel(
            name='BSCPair',
            fields=[
                ('id', models.BigAutoField(
                            auto_created=True, 
                            primary_key=True, 
                            serialize=False, 
                            verbose_name='ID'
                            )),
                ('created_at', models.DateTimeField(auto_created=True)),
                ('factory_address', models.CharField(max_length=42)),
                ('pair_address', models.CharField(max_length=42, unique=True)),
                ('pair_symbol', models.CharField(max_length=12, unique=True)),
                ('token0', models.CharField(max_length=42)),
                ('token1', models.CharField(max_length=42)),
            ],
            options={
                'db_table': 'BSCPair',
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='BSCPairTransaction',
            fields=[
                ('id', models.BigAutoField(
                    auto_created=True, 
                    primary_key=True, 
                    serialize=False, 
                    verbose_name='ID'
                    )),
                ('reserveToken0', models.CharField(default=0, max_length=256)),
                ('reserveToken1', models.CharField(default=0, max_length=256)),
                ('amount0In', models.CharField(max_length=256, null=True)),
                ('amount1In', models.CharField(max_length=256, null=True)),
                ('amount0Out', models.CharField(max_length=256, null=True)),
                ('amount1Out', models.CharField(max_length=256, null=True)),
                ('maker_address', models.CharField(max_length=42)),
                ('pair', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='blockchains.bscpair')),
            ],
            options={
                'db_table': 'BSCPairTransaction',
                'abstract': False,
            },
        ),
    ]
