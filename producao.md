# Colocar a aplicação django em produção

## 1. Configurar o ambiente

•	Crie um ambiente virtual:
``` 
python3 -m venv venv
source venv/bin/activate
```
•	Instale as dependências:
```
pip install -r requirements.txt
```
•	Configure o arquivo .env (se necessário) para armazenar as variáveis de ambiente (e.g., DEBUG=False, ALLOWED_HOSTS, configurações do banco de dados, etc.).

--
## 2. Preparar o Django para produção

•	Configure o settings.py:
o	Coloque DEBUG = False.
o	Configure os ALLOWED_HOSTS com os domínios ou IPs permitidos.
o	Ative o uso de arquivos estáticos e mídias:
```python
# settings.py
STATIC_ROOT = BASE_DIR / 'staticfiles'
MEDIA_ROOT = BASE_DIR / 'mediafiles'
```
•	Coletar os arquivos estáticos:
```bash
python manage.py collectstatic
```

--
## 3. Usar o Gunicorn como servidor WSGI

•	Instale o Gunicorn:
```
pip install gunicorn
```
•	Teste o servidor localmente:
```
gunicorn myproject.wsgi:application --bind 127.0.0.1:8000
```

--
## 4. Criar um serviço systemd

Isso garante que a aplicação será iniciada automaticamente no boot.
•	Crie o arquivo de serviço em /etc/systemd/system/myproject.service:
```
# sistema_solicitacoes.service
[Unit]
Description=Gunicorn instance to serve myproject
After=network.target

[Service]
User=seu_usuario
Group=www-data
WorkingDirectory=/caminho/para/seu/projeto
ExecStart=/caminho/para/seu/projeto/venv/bin/gunicorn --workers 3 --bind unix:/caminho/para/seu/projeto/myproject.sock myproject.wsgi:application

[Install]
WantedBy=multi-user.target
```
•	Ative e inicie o serviço:
```
sudo systemctl start myproject
sudo systemctl enable myproject
```

--
## 5. Configurar Nginx

•	Certifique-se de que o Nginx está configurado para fazer proxy para o socket Unix do Gunicorn.

