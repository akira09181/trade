# Generated by Django 3.1.6 on 2022-02-08 10:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mytrade', '0005_auto_20211127_2057'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bre',
            name='sjpy',
            field=models.IntegerField(default=10, verbose_name='初期の投資額'),
        ),
    ]
