# Generated by Django 5.0.10 on 2025-02-13 13:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('solicitacoes', '0003_produto_c1_rateio'),
    ]

    operations = [
        migrations.AddField(
            model_name='produto',
            name='ctj_desc',
            field=models.CharField(default='', max_length=40),
        ),
        migrations.AlterField(
            model_name='produto',
            name='c1_rateio',
            field=models.CharField(default='2', max_length=1),
        ),
    ]
