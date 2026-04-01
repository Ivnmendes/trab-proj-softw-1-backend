import pdfplumber
import pandas as pd


def extrair_remume(caminho_pdf, caminho_csv):
    dados_totais = []
    colunas_alvo = ["Nome", "Concentração", "Forma Farmacêutica", "Componente", "Postos de Distribuição", "Status"]

    print("Iniciando a extração do PDF...")

    with pdfplumber.open(caminho_pdf) as pdf:
        for numero_pagina, pagina in enumerate(pdf.pages):
            tabelas = pagina.extract_tables()

            for tabela in tabelas:
                if tabela and "Nome" in str(tabela[0]):

                    for linha in tabela[1:]:
                        linha_limpa = [str(celula).replace('\n', ' ').strip() if celula else '' for celula in linha]

                        if len(linha_limpa) == 6:
                            dados_totais.append(linha_limpa)

    print(f"Extração concluída. {len(dados_totais)} linhas brutas encontradas.")

    df = pd.DataFrame(dados_totais, columns=colunas_alvo)

    import numpy as np
    df.replace('', np.nan, inplace=True)

    colunas_para_preencher = ["Nome", "Concentração", "Forma Farmacêutica", "Componente", "Status"]
    df[colunas_para_preencher] = df[colunas_para_preencher].ffill()

    df = df.groupby(colunas_para_preencher, dropna=False)['Postos de Distribuição'].apply(
        lambda x: ' '.join(x.dropna())
    ).reset_index()

    df = df[colunas_alvo]

    df.to_csv(caminho_csv, index=False, encoding='utf-8-sig', sep=';')
    print(f"Sucesso! Tabela limpa salva em: {caminho_csv}")


# arquivos
arquivo_entrada = 'remume.pdf'
arquivo_saida = 'medicamentos_estruturados.csv'

extrair_remume(arquivo_entrada, arquivo_saida)