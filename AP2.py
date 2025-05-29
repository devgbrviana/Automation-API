import requests
import sqlite3
from bs4 import BeautifulSoup
from openpyxl import Workbook
from openpyxl.styles import Font
from datetime import datetime 


print("Digite os nomes dos países em INGLÊS e sem acentos.")

entrada = input("Digite 3 países em inglês (separados por vírgula): ")
listaDePaises = entrada.split(',')
listaDePaises = [pais.strip() for pais in listaDePaises]


dados_paises = []

for pais in listaDePaises:
    url = f'https://restcountries.com/v3.1/name/{pais}'
    response = requests.get(url)

    if response.status_code != 200:
        print(f"Erro: Não foi possível encontrar dados de '{pais}'.")
        continue

    dados = response.json()
    if not dados:
        print(f"Nenhum dado encontrado para '{pais}'.")
        continue

    info = dados[0]
    try:
        nomeComum = info['name']['common']
        nomeOficial = info['name']['official']
        capital = info['capital'][0] if 'capital' in info else 'N/A'
        regiao = info['region']
        subRegiao = info['subregion']
        populacao = info['population']
        area = info['area']
        moeda_info = list(info['currencies'].values())[0]
        moedaNome = moeda_info['name']
        moedaSimbolo = moeda_info['symbol']
        idioma = str(info.get('languages', 'N/A'))
        fusoHorario = info['timezones'][0]
        bandeira = info["flags"]['png']

        dados_paises.append([
            nomeComum, nomeOficial, capital, regiao, subRegiao, populacao,
            area, moedaNome, moedaSimbolo, idioma, fusoHorario, bandeira
        ])

        print("Dados exibidos:")
        print(f"Nome Comum: {nomeComum}")
        print(f"Nome Oficial: {nomeOficial}")
        print(f"Capital: {capital}")
        print(f"Região: {regiao}")
        print(f"SubRegião: {subRegiao}")
        print(f"População: {populacao}")
        print(f"Área: {area} km²")
        print(f"Moeda: {moedaNome} ({moedaSimbolo})")
        print(f"Idiomas: {idioma}")
        print(f"Fuso Horário: {fusoHorario}")
        print(f"Bandeira: {bandeira}")
        print('<------------------------------------------->')

     
        conexao = sqlite3.connect("paises.db")
        cursor = conexao.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS paises (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nomeComum TEXT,
                nomeOficial TEXT,
                capital TEXT,
                regiao TEXT,
                subRegiao TEXT,
                populacao INTEGER,
                area REAL,
                moedaNome TEXT,
                moedaSimbolo TEXT,
                idioma TEXT,
                fusoHorario TEXT,
                bandeira TEXT
            )
        ''')
        cursor.execute('''
            INSERT INTO paises (
                nomeComum, nomeOficial, capital, regiao, subRegiao,
                populacao, area, moedaNome, moedaSimbolo, idioma,
                fusoHorario, bandeira
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            nomeComum, nomeOficial, capital, regiao, subRegiao, populacao,
            area, moedaNome, moedaSimbolo, idioma, fusoHorario, bandeira
        ))
        conexao.commit()
        conexao.close()

    except Exception as e:
        print(f"Erro ao processar os dados de '{pais}': {e}")


def extrairLivros():
    try:
        url = "https://books.toscrape.com"
        response = requests.get(url)
        if response.status_code != 200:
            return []

        soup = BeautifulSoup(response.text, "html.parser")
        livros = []

        for artigo in soup.find_all("article", class_="product_pod"):
            titulo = artigo.h3.a["title"]
            preco = artigo.find("p", class_="price_color").text.strip()
            avaliacao = artigo.find("p", class_="star-rating")["class"][1]
            disponibilidade = artigo.find("p", class_="instock availability").text.strip()

            livros.append({
                "titulo": titulo,
                "preco": preco,
                "avaliacao": avaliacao,
                "disponibilidade": disponibilidade
            })

            print("Dados exibidos:")
            print(f"Título: {titulo}")
            print(f"Preço: {preco}")
            print(f"Avaliação: {avaliacao}")
            print(f"Disponibilidade: {disponibilidade}")
            print('<------------------------------------------->')

        return livros[:10]

    except Exception as e:
        print(f"Erro ao extrair livros: {e}")
        return []


def salvarLivrosNoDB(livros):
    conexao = sqlite3.connect("livraria.db")
    cursor = conexao.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS livros (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titulo TEXT,
            preco REAL,
            avaliacao TEXT,
            disponibilidade TEXT
        )
    ''')

    for livro in livros:
        cursor.execute('''
            INSERT INTO livros(titulo, preco, avaliacao, disponibilidade)
            VALUES (?, ?, ?, ?)
        ''', (livro['titulo'], livro['preco'], livro['avaliacao'], livro['disponibilidade']))

    conexao.commit()
    conexao.close()


livros_extraidos = extrairLivros()
if livros_extraidos:
    salvarLivrosNoDB(livros_extraidos)


wb = Workbook()

#Planilha de países
planilha1 = wb.active
planilha1.title = "Paises"
cabecalhos_paises = ["Nome Comum", "Nome Oficial", "Capital", "Região", "SubRegião",
                     "População", "Área", "Nome Moeda", "Símbolo Moeda", "Idioma", "Fuso Horário", "Bandeira"]
planilha1.append(["Nome Dupla:", "Kaio Mungo e Luiz Henrique"])
planilha1.append(["Data de Geração:", datetime.now().strftime("%d/%m/%Y")])
planilha1.append(cabecalhos_paises)

for linha in dados_paises:
    planilha1.append(linha)

for cell in planilha1[1]:
    cell.font = Font(bold=True)

for cell in planilha1[2]:
    cell.font = Font(bold=True)

for cell in planilha1[3]:
    cell.font = Font(color="a2c5ac", bold=True)


#Planilha de livros
planilha2 = wb.create_sheet(title="Livros")
cabecalhos_livros = ["Título", "Preço", "Avaliação", "Disponibilidade"]
planilha2.append(cabecalhos_livros)

for livro in livros_extraidos:
    planilha2.append([
        livro["titulo"],
        livro["preco"],
        livro["avaliacao"],
        livro["disponibilidade"]
    ])
for cell in planilha2[1]:
    cell.font = Font(color="a2c5ac", bold=True)

wb.save("dados.xlsx")
print("Arquivo Excel 'dados.xlsx' criado com sucesso.")
