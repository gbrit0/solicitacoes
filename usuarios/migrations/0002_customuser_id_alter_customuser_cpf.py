# Generated by Django 5.0.10 on 2025-01-02 17:46

import utils.cpf_funcs
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usuarios', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='id',
            field=models.CharField(default=None, editable=False, max_length=6, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='cpf',
            field=models.CharField(max_length=14, unique=True, validators=[utils.cpf_funcs.cpf_validate]),
        ),
    ]
