import pdfplumber
import pandas as pd
import re


def extrair_farmacia_digital(caminho_pdf, caminho_csv):
    dados_totais = []
    colunas_alvo = ["Nome", "Concentração", "Forma Farmacêutica", "Componente", "Postos de Distribuição", "Status"]

    print("Iniciando a extração do PDF da Farmácia Digital RS...")

    with pdfplumber.open(caminho_pdf) as pdf:
        for pagina in pdf.pages:
            tabelas = pagina.extract_tables()

            for tabela in tabelas:
                if tabela:
                    for linha in tabela:
                        if not linha or not linha[0]:
                            continue

                        texto_medicamento = str(linha[0]).replace('\n', ' ').strip()

                        if "NOME DO MEDICAMENTO" in texto_medicamento:
                            continue

                        nome = texto_medicamento
                        concentracao = ""
                        forma = ""

                        match_forma = re.search(r'\((.*?)\)', texto_medicamento)
                        if match_forma:
                            forma = match_forma.group(1).replace('por ', '').strip()
                            nome = texto_medicamento[:match_forma.start()].strip()

                        match_num = re.search(r'\d', nome)
                        if match_num:
                            concentracao = nome[match_num.start():].strip()
                            nome = nome[:match_num.start()].strip()

                        componente = "Especializado"
                        postos = "Farmácia Digital RS"
                        status = ""

                        dados_totais.append([nome, concentracao, forma, componente, postos, status])

    df = pd.DataFrame(dados_totais, columns=colunas_alvo)

    df = df[df['Nome'].astype(bool)]

    df.to_csv(caminho_csv, index=False, encoding='utf-8-sig', sep=';')
    print(f"Sucesso! {len(df)} linhas extraídas e formatadas. Salvo em: {caminho_csv}")


# arquivos
arquivo_entrada = 'farmadigital.pdf'
arquivo_saida = 'farmacia_digital_estruturada.csv'

extrair_farmacia_digital(arquivo_entrada, arquivo_saida)