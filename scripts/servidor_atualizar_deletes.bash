#! /bin/bash
cd /home/bot/solicitacoes
while :
do
   cd /home/bot/solicitacoes
   printf "\n$(date) Deleção de Solicitações de Compras Inicializada\n"
   source venv/bin/activate
   python manage.py shell
   from setup.utils.sync import sincronizar_itens_deletados
   sincronizar_itens_deletados()
   printf "$(date) Deleção de Solicitações de Compras Finalizada\n"
   sleep 900
done