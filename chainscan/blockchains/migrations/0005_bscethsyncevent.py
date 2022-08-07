# Generated by Django 4.0.6 on 2022-08-07 05:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blockchains', '0004_delete_bsctransaction_remove_bscpair_created_at_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='BscEthSyncEvent',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('updated_at', models.DateTimeField(auto_created=True, null=True)),
                ('reserve0', models.CharField(default=0, max_length=256)),
                ('reserve1', models.CharField(default=0, max_length=256)),
                ('hash', models.CharField(max_length=66, null=True)),
                ('block_number', models.IntegerField(null=True)),
                ('transaction_index', models.IntegerField(null=True)),
                ('pair_address', models.CharField(max_length=42)),
                ('method', models.CharField(max_length=66)),
            ],
            options={
                'db_table': 'BscEthSyncEvent',
                'abstract': False,
            },
        ),
    ]
