# Generated by Django 5.0.10 on 2024-12-23 17:08

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('solicitacoes', '0002_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='solicitacao',
            name='c1_emissao',
            field=models.CharField(default=django.utils.timezone.now, max_length=8),
        ),
        migrations.AlterField(
            model_name='solicitacao',
            name='c1_datprf',
            field=models.CharField(max_length=8),
        ),
    ]
