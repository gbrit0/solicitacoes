# Como servir os arquivos estáticos da aplicação no Gunicorn

O Django Admin é uma interface padrão do Django que permite a administração dos modelos e aplicações dentro de um projeto. Como faz parte da biblioteca, sua implementação em produção requer algumas etapas. Inicialmente, é necessário coletar os arquivos estáticos e disponibilizá-los na pasta `static` do projeto por meio do comando:

```bash
python3 manage.py collectstatic

```

A aplicação deve fornecer uma URL e um diretório raiz para os arquivos estáticos, configurados no arquivo settings.py:

```python
# settings.py
STATIC_URL = '/static/'

STATIC_ROOT = os.path.join(BASE_DIR, 'static')
```

Contudo, apenas a configuração acima não garante que os arquivos estáticos estarão disponíveis. Como não é recomendado servir aplicações Django diretamente com o comando:

```
python3 manage.py runserver
``` 

A aplicação deve ser colocada atrás de um servidor WSGI para produção.

## Servindo Arquivos Estáticos com Gunicorn e Nginx

O Gunicorn é um servidor HTTP para aplicações Python, frequentemente utilizado como servidor de aplicação para frameworks como Django e Flask. Entretanto, ele não fornece suporte nativo para arquivos estáticos, sendo necessário configurá-lo por trás de um proxy reverso, como o Nginx.

O servidor da API BRG utiliza Nginx como proxy reverso. Este servidor realiza o roteamento para um servidor secundário localizado na Grid, onde o sistema de solicitações é executado. Assim, a configuração do Nginx no servidor principal deve incluir uma referência aos arquivos estáticos da aplicação Django:

```nginx
server {
   listen 55001; # porta em que foi configurada a aplicação no servidor grid
   location /static/ { # referência aos arquivos estáticos da aplicação django
      proxy_pass http://127.0.0.1:55001/static/; 
   }
}
```

No servidor Grid, onde o Django e Gunicorn estão em execução, é necessário configurar o Nginx para servir arquivos estáticos e rotear as solicitações da aplicação para o Gunicorn.

### Configuração do Nginx no Servidor Grid

No servidor Grid, o Nginx deve escutar uma porta específica para servir os arquivos estáticos e encaminhar as solicitações para o Gunicorn. A configuração é a seguinte:

```nginx
server {
    listen 55001;
    server_name 192.168.15.60;

    # Configurar o diretório de arquivos estáticos
    location /static/ {
        root /home/bot/solicitacoes/;
        autoindex off;  # Desativa a listagem de arquivos no diretório
    }

    # Encaminhar requisições para o Gunicorn
    location / {
        proxy_pass http://127.0.0.1:55002;  # Porta onde o Gunicorn está escutando
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}

```

### Configurando o Gunicorn

O Gunicorn deve ser configurado para escutar em uma porta diferente da usada pelo Nginx (no exemplo acima, 55002). Para iniciar o Gunicorn:

```bash
gunicorn setup.wsgi:application --bind 0.0.0.0:55002

```

### Testando a Configuração

Após configurar o Nginx e o Gunicorn, teste as configurações do Nginx:

```bash
sudo nginx -t
```

Se não houverem erros, reinicie o Nginx:

```bash
sudo systemctl restart nginx
```

Por fim, acesse a aplicação para verificar se os arquivos estáticos estão sendo carregados corretamente.

