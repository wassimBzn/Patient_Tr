# Generated by Django 3.2.6 on 2021-12-20 01:44

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='antecedentes',
            name='id',
            field=models.AutoField(default=20122021246, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='consultation',
            name='Date_de_consultation',
            field=models.DateTimeField(default=datetime.datetime(2021, 12, 20, 2, 44, 46, 586586)),
        ),
        migrations.AlterField(
            model_name='consultation',
            name='Prochaine_Rondez_vous',
            field=models.DateTimeField(default=datetime.datetime(2021, 12, 20, 2, 44, 46, 586586)),
        ),
        migrations.AlterField(
            model_name='consultation',
            name='id',
            field=models.AutoField(default=20122021246, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='examen_clinique',
            name='id',
            field=models.AutoField(default=20122021246, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='examen_phisique',
            name='id',
            field=models.AutoField(default=20122021246, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='habitude',
            name='id',
            field=models.AutoField(default=20122021246, primary_key=True, serialize=False),
        ),
    ]
