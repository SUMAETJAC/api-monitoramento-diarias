# api-monitoramento-diarias
Teste do download de Monitoramento Diarias

# 📄 API de Exportação - Monitoramento de Diárias (TJAC)

Esta é uma API REST construída em Python com o microframework Flask. O objetivo principal deste serviço é atuar como uma "ponte" entre o painel de Monitoramento de Diárias construído no Power BI e o banco de dados (neste caso, espelhado via Google Sheets). 

A API recebe parâmetros de filtro dinâmicos através da URL, processa os dados em tempo real e devolve um arquivo Excel (`.xlsx`) pronto para download pelo usuário final.

## 🛠️ Tecnologias Utilizadas
* **Python 3:** Linguagem principal do projeto.
* **Flask:** Microframework web para criar a rota de download da API.
* **Pandas:** Biblioteca de manipulação de dados utilizada para ler o CSV e aplicar os filtros.
* **Openpyxl:** Motor (engine) utilizado pelo Pandas para gerar arquivos no formato Excel (`.xlsx`).
* **Gunicorn:** Servidor HTTP de produção (WSGI) utilizado para o deploy no Render.

## ⚙️ Como o Código Funciona (Lógica do `app.py`)

O arquivo `app.py` segue um fluxo de 5 etapas sempre que um usuário clica no botão de download no Power BI:

### 1. Leitura da Fonte de Dados
A API consome os dados diretamente de uma URL do Google Sheets formatada para exportar em CSV. O Pandas (`pd.read_csv`) transforma esse arquivo em um DataFrame, que é uma tabela de dados em memória.

### 2. Captura de Parâmetros (Filtros)
O Power BI envia os filtros selecionados pelo usuário através da URL (ex: `?comarca=RIO BRANCO&ano=2026`). O Flask utiliza o `request.args.get()` para ler esses valores. Se o usuário não filtrou nada no painel, o valor padrão recebido é `'Todos'`.

### 3. Aplicação dos Filtros
O Pandas percorre as colunas da tabela e aplica os filtros recebidos:
* **Filtros de Texto Exato:** Comarca, Rubrica, Tipo de Diária e Unidade são filtrados comparando o texto exato. Existe uma trava de segurança (`'Coluna' in df.columns`) para evitar que a API quebre caso o nome da coluna mude na origem.
* **Tratamento Inteligente de Datas:** Como a base de dados possui apenas a coluna `Data Empenho` (formato dd/mm/aaaa), mas o painel filtra por `Ano` e `Mês` separadamente, o código converte a coluna de texto para o formato de data (`pd.to_datetime`) e extrai o Ano e o Mês dinamicamente para aplicar o filtro correto.

### 4. Geração do Arquivo em Memória
Para evitar salvar arquivos físicos no servidor (o que consumiria espaço e causaria conflitos entre múltiplos usuários baixando ao mesmo tempo), utilizamos a biblioteca `io.BytesIO()`. O arquivo Excel é gerado temporariamente na memória RAM do servidor.

### 5. Resposta HTTP (Download)
A função `send_file` do Flask pega esse arquivo em memória e o envia para o navegador do usuário com os cabeçalhos corretos (`mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"`), forçando o navegador a iniciar o download de um arquivo chamado `Relatorio_Diarias_Filtrado.xlsx`.

## 🚀 Como Rodar Localmente (Para Desenvolvimento)

1. Clone o repositório.
2. Crie um ambiente virtual: `python -m venv venv`
3. Ative o ambiente virtual (Windows: `venv\Scripts\activate` | Linux/Mac: `source venv/bin/activate`)
4. Instale as dependências: `pip install -r requirements.txt`
5. Execute a aplicação: `python app.py`

A API ficará disponível em `http://localhost:5000`. 
Para testar, acesse no navegador: `http://localhost:5000/download?comarca=SENA MADUREIRA`

## ☁️ Deploy no Render
Este projeto está configurado para deploy imediato na plataforma Render.
* **Build Command:** `pip install -r requirements.txt`
* **Start Command:** `gunicorn app:app`


#Imagem Conceitual:
<img width="1990" height="1379" alt="image" src="https://github.com/user-attachments/assets/02866cb4-5e33-4728-86dd-c36fe23e5bdf" />


