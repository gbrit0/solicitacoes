# Generated by Django 5.0.10 on 2025-02-21 18:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('solicitacoes', '0012_statussc1_delete'),
    ]

    operations = [
        migrations.AlterField(
            model_name='statussc1',
            name='delete',
            field=models.CharField(db_column='D_E_L_E_T_', default='', max_length=1),
        ),
    ]
