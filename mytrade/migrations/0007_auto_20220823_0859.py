# Generated by Django 3.1.1 on 2022-08-22 23:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mytrade', '0006_auto_20220208_1935'),
    ]

    operations = [
        migrations.AddField(
            model_name='bre',
            name='term_from',
            field=models.DateField(default='2020-01-01', verbose_name='~から'),
        ),
        migrations.AddField(
            model_name='bre',
            name='term_to',
            field=models.DateField(default='2021-01-01', verbose_name='~まで'),
        ),
        migrations.AddField(
            model_name='sma',
            name='term_from',
            field=models.DateField(default='2020-01-01', verbose_name='~から'),
        ),
        migrations.AddField(
            model_name='sma',
            name='term_to',
            field=models.DateField(default='2021-01-01', verbose_name='~まで'),
        ),
        migrations.AlterField(
            model_name='bre',
            name='sjpy',
            field=models.IntegerField(default=100000, verbose_name='初期の投資額'),
        ),
    ]