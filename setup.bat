@echo off

:: Atualizar e instalar dependências
:: echo Instalando Python
:: choco install python --version 3.9.0 -y
:: choco install postgresql --version 13.0 -y

:: Criar um diretório para o projeto
mkdir "%USERPROFILE%\api_tarefas_aps"
cd "%USERPROFILE%\api_tarefas_aps"

:: Criar um ambiente virtual
python -m venv venv
call venv\Scripts\activate

:: Instalar as dependências necessárias
pip install -r requirements.txt

:: Instruções para configurar o banco de dados
echo Por favor, configure o PostgreSQL:
echo 1. Acesse o psql: psql -U postgres
echo 2. Crie o banco: CREATE DATABASE tarefas;
echo 3. Conectar ao banco de dados 'tarefas': \c tarefas
echo 4. Executar os scripts presents na pasta sql: \i sql/criar_tabelas.sql, \i sql/criar_view.sql, \i sql/criar_funcoes.sql, \i sql/criar_procedures.sql, \i sql/criar_triggers.sql
echo 5. Para sair do psql, use \q

pause
