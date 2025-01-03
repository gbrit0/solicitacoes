# Generated by Django 5.0.10 on 2024-12-31 13:20

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('solicitacoes', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='solicitacao',
            name='user',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='produto',
            name='c1_num',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.DO_NOTHING, to='solicitacoes.solicitacao'),
        ),
    ]
