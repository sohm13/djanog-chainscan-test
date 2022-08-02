# Generated by Django 4.0.6 on 2022-07-08 12:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blockchains', '0003_bscpair_bscpairtransaction'),
    ]

    operations = [
        migrations.DeleteModel(
            name='BSCTransaction',
        ),
        migrations.RemoveField(
            model_name='bscpair',
            name='created_at',
        ),
        migrations.AddField(
            model_name='bscpair',
            name='updated_at',
            field=models.DateTimeField(auto_created=True, null=True),
        ),
        migrations.AddField(
            model_name='bscpairtransaction',
            name='block_number',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='bscpairtransaction',
            name='hash',
            field=models.CharField(max_length=66, null=True),
        ),
        migrations.AddField(
            model_name='bscpairtransaction',
            name='updated_at',
            field=models.DateTimeField(auto_created=True, null=True),
        ),
    ]
