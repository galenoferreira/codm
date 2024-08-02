### Passo 1: Criar um Projeto Django

1. **Instalar Django e boto3**:
   ```sh
   pip install django boto3
   ```

2. **Criar um novo projeto Django**:
   ```sh
   django-admin startproject myproject
   cd myproject
   ```

3. **Criar um novo aplicativo dentro do projeto**:
   ```sh
   python manage.py startapp presignedurl
   ```

4. **Adicionar o aplicativo ao `INSTALLED_APPS` no `settings.py`**:
   ```python
   # myproject/settings.py
   INSTALLED_APPS = [
       ...
       'presignedurl',
   ]
   ```

### Passo 2: Configurar o Aplicativo Django

1. **Adicionar as configurações da AWS no `settings.py`**:
   ```python
   # myproject/settings.py
   AWS_ACCESS_KEY_ID = 'your_access_key'
   AWS_SECRET_ACCESS_KEY = 'your_secret_key'
   AWS_STORAGE_BUCKET_NAME = 'galeno-codm-dev-codm'
   ```

2. **Criar a visualização para gerar a URL pré-assinada**:
   ```python
   # presignedurl/views.py
   from django.conf import settings
   from django.http import JsonResponse
   from django.views import View
   import boto3

   class GeneratePresignedUrlView(View):
       def post(self, request):
           file_name = request.POST.get('file_name')
           expiration = 120  # URL válida por 2 minutos

           s3 = boto3.client(
               's3',
               aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
               aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY
           )

           try:
               presigned_url = s3.generate_presigned_url(
                   'put_object',
                   Params={'Bucket': settings.AWS_STORAGE_BUCKET_NAME, 'Key': file_name},
                   ExpiresIn=expiration
               )
               return JsonResponse({'presigned_url': presigned_url}, status=200)
           except Exception as e:
               return JsonResponse({'error': str(e)}, status=500)
   ```

3. **Adicionar a URL da visualização**:
   ```python
   # presignedurl/urls.py
   from django.urls import path
   from .views import GeneratePresignedUrlView

   urlpatterns = [
       path('generate-presigned-url/', GeneratePresignedUrlView.as_view(), name='generate_presigned_url'),
   ]
   ```

4. **Incluir as URLs do aplicativo no URLconf principal**:
   ```python
   # myproject/urls.py
   from django.contrib import admin
   from django.urls import path, include

   urlpatterns = [
       path('admin/', admin.site.urls),
       path('presignedurl/', include('presignedurl.urls')),
   ]
   ```

### Passo 3: Testar Localmente

1. **Executar o servidor Django**:
   ```sh
   python manage.py runserver
   ```

2. **Fazer uma solicitação POST para testar a geração da URL pré-assinada**:
   ```sh
   curl -X POST http://127.0.0.1:8000/presignedurl/generate-presigned-url/ -d "file_name=testfile.txt"
   ```

### Passo 4: Implementar na AWS

#### Opção 1: Usando AWS Elastic Beanstalk

1. **Instalar a CLI do Elastic Beanstalk**:
   ```sh
   pip install awsebcli
   ```

2. **Inicializar o Ambiente Elastic Beanstalk**:
   ```sh
   eb init -p python-3.8 myproject
   ```

3. **Criar e Implantar o Ambiente**:
   ```sh
   eb create myproject-env
   eb deploy
   ```

#### Opção 2: Usando AWS EC2

1. **Lançar uma Instância EC2**

   - No Console AWS, vá para EC2 e lance uma nova instância.
   - Escolha uma Amazon Linux 2 AMI.
   - Configure a instância com as especificações desejadas.
   - Configure as regras de segurança para permitir tráfego HTTP (porta 80).

2. **Configurar a Instância**

   - Conecte-se à instância EC2 via SSH.
   - Instale as dependências necessárias:
     ```sh
     sudo yum update -y
     sudo yum install python3 -y
     sudo pip3 install django boto3
     ```

   - Copie os arquivos do projeto Django para a instância.

3. **Configurar o Servidor Django**

   - Execute as migrações e inicie o servidor Django:
     ```sh
     python3 manage.py migrate
     python3 manage.py runserver 0.0.0.0:8000
     ```

4. **Configurar um Serviço de Sistema para Django**

   - Crie um arquivo de serviço systemd para garantir que a aplicação Django seja iniciada automaticamente:
     ```sh
     sudo nano /etc/systemd/system/djangoapp.service
     ```

     Adicione o seguinte conteúdo:
     ```ini
     [Unit]
     Description=Gunicorn instance to serve my Django app
     After=network.target

     [Service]
     User=ec2-user
     Group=nginx
     WorkingDirectory=/home/ec2-user/myproject
     Environment="PATH=/home/ec2-user/myproject/venv/bin"
     ExecStart=/usr/local/bin/gunicorn --workers 3 --bind 0.0.0.0:8000 myproject.wsgi:application

     [Install]
     WantedBy=multi-user.target
     ```

   - Habilite e inicie o serviço:
     ```sh
     sudo systemctl start djangoapp
     sudo systemctl enable djangoapp
     ```

### Passo 5: Testar o Endpoint na AWS

Faça uma solicitação POST para o endpoint do Elastic Beanstalk ou o endereço público da instância EC2 para garantir que a API está funcionando corretamente.

```sh
curl -X POST http://<seu-endpoint>/presignedurl/generate-presigned-url/ -d "file_name=testfile.txt"
```

Seguindo esses passos, você pode configurar sua API Django para gerar URLs pré-assinadas e implementá-la na AWS.