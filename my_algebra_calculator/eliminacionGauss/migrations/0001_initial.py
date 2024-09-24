# Generated by Django 4.2.16 on 2024-09-24 15:35

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Ope_combinadas',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('OpV_NmVectores', models.IntegerField()),
                ('OpV_DmVectores', models.IntegerField()),
                ('OpV_valor', models.FloatField()),
            ],
            options={
                'unique_together': {('OpV_NmVectores', 'OpV_DmVectores')},
            },
        ),
        migrations.CreateModel(
            name='MltFC_vertical',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('MfcY_NmVectorX', models.IntegerField()),
                ('MfcY_NmVectorY', models.IntegerField()),
                ('MfcY_valor', models.FloatField()),
            ],
            options={
                'unique_together': {('MfcY_NmVectorX', 'MfcY_NmVectorY')},
            },
        ),
        migrations.CreateModel(
            name='MltFC_horizontal',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('MfcX_NmVectorX', models.IntegerField()),
                ('MfcX_NmVectorY', models.IntegerField()),
                ('MfcX_valor', models.FloatField()),
            ],
            options={
                'unique_together': {('MfcX_NmVectorX', 'MfcX_NmVectorY')},
            },
        ),
        migrations.CreateModel(
            name='Elim_Gauss',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('EG_ecuaciones', models.IntegerField()),
                ('EG_incognitas', models.IntegerField()),
                ('EG_fila', models.IntegerField()),
                ('EG_columna', models.IntegerField()),
                ('EG_valor', models.FloatField()),
            ],
            options={
                'unique_together': {('EG_fila', 'EG_columna')},
            },
        ),
    ]
