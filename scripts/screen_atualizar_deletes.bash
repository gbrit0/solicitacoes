#! /bin/bash
screen -XS updateSC quit
screen -dmS updateSC
screen -S updateSC -p 0 -X stuff 'bash /home/bot/solicitacoes/scripts/servidor_atualizar_deletes.bash
'