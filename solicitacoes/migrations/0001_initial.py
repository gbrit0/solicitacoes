# Generated by Django 5.0.10 on 2024-12-27 14:30

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Produto',
            fields=[
                ('c1_item', models.CharField(max_length=4)),
                ('c1_produto', models.CharField(max_length=15)),
                ('c1_descri', models.CharField(max_length=50)),
                ('c1_um', models.CharField(max_length=2)),
                ('c1_local', models.CharField(max_length=2)),
                ('c1_quant', models.DecimalField(decimal_places=2, max_digits=12)),
                ('c1_cc', models.CharField(default='', max_length=60)),
                ('c1_datprf', models.DateField(default='2025-01-01')),
                ('c1_obs', models.CharField(default='', max_length=30)),
                ('r_e_c_n_o', models.BigIntegerField(default=0, primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='Solicitacao',
            fields=[
                ('c1_num', models.CharField(default='', max_length=6, primary_key=True, serialize=False)),
                ('c1_emissao', models.DateField()),
            ],
        ),
    ]
