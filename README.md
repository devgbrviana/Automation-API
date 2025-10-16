# 🚀 Pipeline de Automação de Dados (Automation API)

Este projeto em Python implementa um pipeline de automação de dados de ponta a ponta, que integra coleta de dados de APIs RESTful e Web Scraping, seguido por persistência em banco de dados SQLite e exportação para Excel.

O script principal (`AP2.py`) foi desenvolvido pela dupla **Gabriel Viana e Fábio Garrote** (conforme metadados de exemplo).

## ✨ Funcionalidades do Pipeline

O pipeline executa duas tarefas principais de coleta de dados de diferentes fontes:

### 1. Coleta de Dados de Países (API RESTful)

* **Fonte:** API `https://restcountries.com/`.
* **Entrada:** O usuário deve fornecer 3 nomes de países em inglês, separados por vírgula.
* **Dados Coletados:** Nome Comum, Nome Oficial, Capital, Região, População, Área, Moeda, Símbolo da Moeda, Idiomas, Fuso Horário e Bandeira (URL).
* **Persistência:** Os dados são armazenados no banco de dados SQLite **`paises.db`** na tabela `paises`.

### 2. Coleta de Dados de Livros (Web Scraping)

* **Fonte:** Site `https://books.toscrape.com`.
* **Ação:** Extrai dados dos 10 primeiros livros listados na página inicial.
* **Dados Coletados:** Título, Preço, Avaliação (em palavras) e Disponibilidade.
* **Persistência:** Os dados são armazenados no banco de dados SQLite **`livraria.db`** na tabela `livros`.

## 📊 Exportação Final (Excel)

Após a coleta e o armazenamento, os dados são consolidados em um único arquivo Excel:

* **Arquivo de Saída:** `dados.xlsx`.
* **Aba "Paises":** Contém os dados da API de países, incluindo metadados da dupla e data de geração.
* **Aba "Livros":** Contém os dados extraídos via Web Scraping.
* **Formatação:** O arquivo utiliza estilos de fonte em negrito e cores para formatar os cabeçalhos.

## 🛠️ Tecnologias Utilizadas

O projeto depende das seguintes bibliotecas Python:

* **`requests`:** Para realizar chamadas à API e requisições HTTP.
* **`BeautifulSoup` (`bs4`):** Para fazer o parse do HTML e extrair os dados do web scraping.
* **`sqlite3`:** Módulo nativo para manipulação dos bancos de dados SQLite.
* **`openpyxl`:** Para criar e gerenciar o arquivo Excel (`.xlsx`).

## ⚙️ Como Configurar e Executar

### 1. Instalação de Dependências

Certifique-se de ter o Python 3 instalado e execute o seguinte comando para instalar as bibliotecas necessárias:

```bash
pip install requests beautifulsoup4 openpyxl

Execute o script principal no seu terminal:

Bash

python AP2.py
