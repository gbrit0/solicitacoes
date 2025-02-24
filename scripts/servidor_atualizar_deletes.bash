#! /bin/bash
cd /home/bot/solicitacoes
while :
do
   cd /home/bot/solicitacoes
   printf "\n$(date) Deleção de Solicitações de Compras Inicializada\n"
   source venv/bin/activate
   python3 solicitacoes/scheduler.py >> deleteSC.log
   printf "$(date) Deleção de Solicitações de Compras Finalizada\n"
   sleep 900
done
