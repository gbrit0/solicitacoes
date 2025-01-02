#! /bin/bash
cd /home/bot/glpi
while:
do
   cd /home/bot/solicitacoes
   # Mata processos gunicorn
   pkill -f "/home/bot/solicitacoes/venv/bin/gunicorn"
   printf "\n$(date) servidor solicitacoes inicializado\n"
   source venv/bin/activate
   gunicorn setup.wsgi:application --bind 0.0.0.0:55001 --timeout 60 >> logs/gunicorn_log.log
   printf "$(date) fim da execução\n"
   sleep 5
done