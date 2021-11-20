# Generated by Django 3.1.6 on 2021-11-20 09:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mytrade', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Bre',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('day', models.IntegerField(default=20, verbose_name='移動平均線（日）')),
                ('val', models.IntegerField(default=30, verbose_name='取引量（％）')),
                ('sjpy', models.IntegerField(default=100000, verbose_name='初期の投資額')),
            ],
        ),
        migrations.CreateModel(
            name='Input',
            fields=[
                ('date', models.DateField(primary_key=True, serialize=False)),
                ('start', models.IntegerField()),
                ('high', models.IntegerField()),
                ('low', models.IntegerField()),
                ('end', models.IntegerField()),
                ('volume', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='Sma',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('short', models.IntegerField(default=5, verbose_name='短い移動平均線')),
                ('long', models.IntegerField(default=14, verbose_name='長い移動平均線')),
                ('val', models.IntegerField(default=30, verbose_name='取引量（％）')),
                ('sjpy', models.IntegerField(default=100000, verbose_name='初期の投資額')),
            ],
        ),
    ]
