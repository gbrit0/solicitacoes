#! /bin/bash
cd /home/gabriel/solicitacoes
while :
do
   cd /home/gabriel/solicitacoes
   # Mata processos gunicorn
   pkill -f "/home/gabriel/solicitacoes/venv/bin/gunicorn"
   printf "\n$(date) Sistema de Solicitacoes inicializado\n"
   source venv/bin/activate
   gunicorn setup.wsgi:application --bind 0.0.0.0:55002 > solicitacoes.log
   printf "$(date) Fim da execução do Sistema de Solicitacoes\n"
   sleep 5
done
