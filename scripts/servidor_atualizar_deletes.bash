#! /bin/bash
cd /home/bot/solicitacoes
while :
do
    printf "\n$(date) Deleção de Solicitações de Compras Inicializada\n"
    source venv/bin/activate
    export DJANGO_SETTINGS_MODULE=setup.settings
    python manage.py runscript sincronizar
    printf "$(date) Deleção de Solicitações de Compras Finalizada\n"
    sleep 900
done
