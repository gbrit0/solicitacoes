# Generated by Django 5.0.10 on 2024-12-22 19:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('solicitacoes', '0003_rename_user_solicitacao_solicitante'),
    ]

    operations = [
        migrations.RenameField(
            model_name='solicitacao',
            old_name='solicitante',
            new_name='user',
        ),
    ]
