# Generated by Django 4.0.6 on 2022-08-13 04:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blockchains', '0004_rename_bsc_block_auroraethsyncevent_block_model_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='bscethsyncevent',
            old_name='bsc_block',
            new_name='block_model',
        ),
        migrations.RenameField(
            model_name='bscethsyncevent',
            old_name='bsc_pair',
            new_name='pair_model',
        ),
    ]