#! /bin/bash
screen -XS solicitacoes quit
screen -dmS solicitacoes
screen -S solicitacoes -p 0 -X stuff 'bash /home/bot/solicitacoes/servidor_solicitacao.bash
'