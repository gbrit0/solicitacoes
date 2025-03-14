# Sistema de Solicitações

Aplicação django para gerar solicitações de compra ao Protheus. Permite visualizar e exportar as solicitações existentes e seus status. A depender do papel do usuário, é possível visualizar apenas as próprias solicitações, usuário padrão, ou todas as solicitações, usuário administrador. Todos os usuários podem gerar solicitações. Apenas administradores podem cadastrar novos usuários.

## Instalação

1. Clone o repositório:
   ```bash
   git clone https://github.com/gbrit0/solicitacoes.git
   ```
2. Crie um ambiente virtual:
   ```bash
   python3 -m venv venv
   ```
3. Ative o ambiente virtual:
   ```bash
   source venv/bin/activate
   ```
4. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```

## Configuração

1. Crie um arquivo `.env` na raiz do projeto e adicione as variáveis de ambiente necessárias:
   ```env
   SECRET_KEY = chave secreta

   USER = usuário de acesso ao banco protheus
   PASSWORD = senha do banco
   HOST = host
   DATABASE = base de dados
   
   ```

2. Aplique as migrações do banco de dados:
   ```bash
   python3 manage.py migrate
   ```

3. Crie um superuser (para acesso ao /admin):
   ```bash
   python3 manage.py createsuperuser
   ```
   
   Insira os dados requisitados.

## Uso

1. [Configure o serviço de arquivos estáticos](servir_arquivos_estaticos.md)

2. Abra uma screen:
   ```bash
   screen -S solicitacoes
   ```

3. Ative o ambiente virtual:
   ```bash
   source venv/bin/activate
   ```

4. Execute o gunicorn:
   ```bash
   gunicorn setup.wsgi:application --bind 0.0.0.0:55002
   ```

5. Acesse a url e o endpoint designado no servidor principal e teste a aplicação.

6. Para visualizar a página de administrador do sistema, acesse <endereço>/admin e logue com as credenciais de superuser criadas [aqui](#configuração).

6. Uma vez que a aplicação esteja funcionando é interessante configurar um crontab para que o serviço seja iniciado sempre que o servidor der reboot:
   ```bash
   crontab -e # acessa o crontab
   ```

   ```bash
   # reboot do servidor de solicitacoes
   @reboot sleep 90 && /bin/bash /caminho/da/aplicacao/scripts/screen_solicitacao.bash >> /caminho/da/aplicacao/logs gunicorn_log.log 2>&1
   ``` 
