# 1 - carregar os dados, mostrando número de registros, colunas e tipos de dados
import pandas as pd

def carregar_dados_de_csv(caminho_arquivo):
        print(f"--> Carregando dados do arquivo: {caminho_arquivo}")
        try:
            # necessário ajustar o separador para ';', com ',' não estava carregando os dados corretamente
            dados = pd.read_csv(caminho_arquivo, encoding='utf-8', sep=';')
            return dados
        except Exception as e:
            print(f"Erro ao carregar o arquivo: {e}")
            return None

def criar_arquivo_csv(caminho_arquivo, dados):
    print(f"--> Criando arquivo CSV: {caminho_arquivo}")
    try:
        dados.to_csv(caminho_arquivo, index=False, encoding='utf-8', sep=';')
        print(f"--> Arquivo CSV criado com sucesso: {caminho_arquivo}")
    except Exception as e:
        print(f"Erro ao criar o arquivo CSV: {e}")

# Exibindo as informações dos dados.
def apresentar_informacoes_dados(dados, etapa):
    print(f'\n-----------{etapa}--------------------')
    print(f"Número de registros: {dados.shape[0]}")
    print(f"Número de colunas: {dados.shape[1]}")
    print("Tipos de dados por coluna:")
    print(dados.dtypes)
    print('-----------------------------------\n')

def remover_colunas_vazias(dados):
    print('\n-----------Removendo Colunas Vazias--------------------')
    colunas_vazias = dados.columns[dados.isnull().all()]
    if len(colunas_vazias) > 0:
        print(f"Colunas vazias encontradas. Total: {len(colunas_vazias)}, nomes: {list(colunas_vazias)}")
        dados = dados.drop(columns=colunas_vazias)
        print(f"Número de colunas após remoção: {dados.shape[1]}")
    else:
        print("Não foram encontradas colunas vazias.")
    return dados

def verificar_e_remover_duplicatas(dados):
    print('\n-----------Verificando Duplicatas--------------------')
    duplicatas = dados.duplicated().sum()
    print(f"Número total de registros: {dados.shape[0]}")
    print(f"Total de registros duplicados: {duplicatas}")
    if duplicatas > 0:
        print('Criando copia dos dados marcados como duplicados para análise...')
        dados_duplicados = dados[dados.duplicated(keep='first')]
        criar_arquivo_csv('backup/dados_duplicados.csv', dados_duplicados)
        print('Removendo registros duplicados...')
        dados_sem_duplicatas = dados.drop_duplicates()
        print(f"Número de registros após remoção de duplicatas: {dados_sem_duplicatas.shape[0]}")
        return dados_sem_duplicatas
    else:
        print("Não foram encontradas duplicatas.")
        return dados

# Verificar como tratar os valores nulos
def verificar_e_tratar_valores_nulos(dados):
    print('\n-----------Verificando Valores Nulos--------------------')
    nulos_por_coluna = dados.isnull().sum()
    print("Número de valores nulos por coluna:")
    print(nulos_por_coluna)
    for coluna in dados.select_dtypes(include=['float64', 'int64']).columns:
        if nulos_por_coluna[coluna] > 0:
            media = dados[coluna].mean()
            dados[coluna].fillna(media, inplace=True)
            print(f"Valores nulos na coluna '{coluna}' foram preenchidos com a média: {media}")
    return dados

# Necessário desenvolver este
def verificar_e_tratar_valores_discrepantes(dados):
    print('\n-----------Verificando Valores Discrepantes--------------------')
    for coluna in dados.select_dtypes(include=['float64', 'int64']).columns:
        q1 = dados[coluna].quantile(0.25)
        q3 = dados[coluna].quantile(0.75)
        iqr = q3 - q1
        limite_inferior = q1 - 1.5 * iqr
        limite_superior = q3 + 1.5 * iqr
        discrepantes = dados[(dados[coluna] < limite_inferior) | (dados[coluna] > limite_superior)]
        print(f"Número de valores discrepantes na coluna '{coluna}': {discrepantes.shape[0]}")
        if discrepantes.shape[0] > 0:
            dados = dados[(dados[coluna] >= limite_inferior) & (dados[coluna] <= limite_superior)]
            print(f"Número de registros após remoção de valores discrepantes na coluna '{coluna}': {dados.shape[0]}")
    return dados

def main():
    caminho_arquivo = 'database/base_varejo.csv'
    dados = carregar_dados_de_csv(caminho_arquivo)
    if dados is None:
        print("Falha ao carregar os dados.")
    else:
        print("-> Dados carregados com sucesso!")
        apresentar_informacoes_dados(dados, "Informações dos dados brutos")
        dados = remover_colunas_vazias(dados)
        dados = verificar_e_remover_duplicatas(dados)
        dados = verificar_e_tratar_valores_nulos(dados)
        dados = verificar_e_tratar_valores_discrepantes(dados)
        apresentar_informacoes_dados(dados, "Informações dos dados após a limpeza")
        print("-> Processamento dos dados concluído!")

if __name__ == "__main__":
    main()