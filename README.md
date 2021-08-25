# boradiscordbot

## Deployment feito com o Heroku CLI

Obs: após criar o app pelo site do heroku:

 - Criar um repositório no github para fazer o upload dos arquivos do app
 - Autenticar a conta do github pelo heroku na aba Deploy
 - Realize o deploy manual nessa mesma aba caso o repositório já tiver todos os arquivos necessários.

### Arquivos necessários para fazer o deploy do app no heroku:

 - requirements.txt (lista com os pacotes do script python, criar com o comando pip freeze > requirements.txt)
 - Procfile (arquivo de configuração do dyno, para o nosso caso só terá a linha "worker: python <nome do script pra rodar>")
 - <nome do script>.py (o próprio script que deve ser rodado)

## Consultando e manipulando os aplicativos no heroku pelo CLI:

Obs: Supondo que já tem o heroku cli instalado

 - Fazer login: heroku login (vai abrir uma página no navegador para realizar o login)
 - Listar os apps instalados: heroku apps
 - Listar os dynos (VMs que rodam a aplicação) disponíveis para o app: heroku ps -a <nome do app>
