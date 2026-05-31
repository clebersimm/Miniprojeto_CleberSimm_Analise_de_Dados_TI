# 1 - carregar os dados, mostrando número de registros, colunas e tipos de dados
import pandas as pd

# Constantes
DADOS_INVALIDOS = "DADOS_INVALIDOS"

# Inicio das funções utilitárias
# Sprint 1 - Importação de dados
def carregar_dados_de_csv(caminho_arquivo):
        print(f"\n------Carregando dados do arquivo: {caminho_arquivo}------")
        try:
            # necessário ajustar o separador para ';', com ',' não estava carregando os dados corretamente
            dados = pd.read_csv(caminho_arquivo, encoding='utf-8', sep=';')
            return dados
        except Exception as e:
            print(f"Erro ao carregar o arquivo: {e}")
            return None

def criar_arquivo_csv(caminho_arquivo, dados):
    print(f"\n------Criando arquivo CSV: {caminho_arquivo}------")
    try:
        dados.to_csv(caminho_arquivo, index=False, encoding='utf-8', sep=';')
        print(f"--> Arquivo CSV criado com sucesso: {caminho_arquivo}")
    except Exception as e:
        print(f"--> Erro ao criar o arquivo CSV: {e}")

# Sprint 1 - Apresentação dos dados
def apresentar_informacoes_dados(dados, etapa):
    print(f'\n------Informações dos dados: {etapa}------')
    print(f"--> Número de registros: {dados.shape[0]}")
    print(f"--> Número de colunas: {dados.shape[1]}")
    print("--> Tipos de dados por coluna:")
    print(dados.dtypes)
    print('------Fim informações dos dados------\n')

# Fim das Funções utilitárias

## Inicio das funções de transformação dos dados

# Sprint 2 - Transformação dos dados - transformar campos de data para tipo datetime
def transforma_campos_tipo_data(dados, coluna):
    print(f'\n------Transformação da coluna "{coluna}" para tipo datetime------')
    dados[coluna] = pd.to_datetime(dados[coluna], dayfirst=True, errors='coerce')
    print(f"--> Coluna '{coluna}' transformada para tipo datetime com sucesso.")
    print(f'------Fim da transformação da coluna "{coluna}" para tipo datetime------\n')

# Sprint 2 - Transformação dos dados - verificar e limpar strings (remover espaços em branco, caracteres especiais, etc.)
def verificar_limpar_strings(dados, colunas):
    print(f'\n------Verificando as colunas {colunas}, para limpeza e normalização dos dados------')
    for coluna in colunas:
        print(f'\n--> Verificando e Limpando Strings na coluna "{coluna}"')
        if coluna in dados.columns and dados[coluna].dtype == 'object':
            dados[coluna] = dados[coluna].astype(str).str.strip().str.upper()  # Remove espaços em branco e converte para maiúsculas
            # função que verifica se existem caracteres especiais na coluna e os remove
            # substitui por string DADOS_INVALIDOS para facilitar a identificação de registros com problemas
            if dados[coluna].str.contains(r'[^\w\s]', regex=True).any():
                print(f"---> Atenção: A coluna '{coluna}' contém caracteres especiais. Marcando os dados inválidos.<---")
            dados[coluna] = dados[coluna].str.replace(r'[^\w\s]', DADOS_INVALIDOS, regex=True)  # Remove caracteres especiais
            print(f"--> Coluna '{coluna}' limpa com sucesso.")
        else:
            print(f"--> Coluna '{coluna}' não encontrada ou não é do tipo string.")
    print(f'\n------Fim da verificação e limpeza das colunas {colunas}------')
    return dados

# Sprint 2 - Transformação dos dados - verificar e limpar inteiros (remover valores inválidos)
def verificar_limpar_inteiros(dados, colunas):
    print(f'\n------Verificando que as colunas {colunas}, são valores inteiros. Se ocorrer que não é valor inteiro será marcado como NaN------')
    for coluna in colunas:
        print(f'\n--> Verificando e Limpando Inteiros na coluna "{coluna}"')
        if coluna in dados.columns:
            # Verifica se existem valores não numéricos usando regex \D (qualquer caractere que não seja dígito)
            if dados[coluna].astype(str).str.contains(r'\D', regex=True).any():
                print(f"---> Atenção: A coluna '{coluna}' contém valores não numéricos. Marcando os dados inválidos.<---")
                dados[coluna] = dados[coluna].astype(str).str.replace(r'\D', 'NaN', regex=True)
            else:
                print(f"--> Coluna '{coluna}' contém apenas números.")
            print(f"--> Coluna '{coluna}' verificada e limpa com sucesso.")
        else:
            print(f"--> Coluna '{coluna}' não encontrada.")
    print(f'\n------Fim da verificação e limpeza das colunas {colunas}------')
    return dados

# Fim das funções de transformação dos dados


# Inicio das funções de limpeza dos dados

# Sprint 3 - Limpeza dos dados
def remover_colunas_vazias(dados):
    print('\n------Removendo Colunas Vazias------')
    colunas_vazias = dados.columns[dados.isnull().all()]
    if len(colunas_vazias) > 0:
        print(f"--> Colunas vazias encontradas. Total: {len(colunas_vazias)}, nomes: {list(colunas_vazias)}")
        dados = dados.drop(columns=colunas_vazias)
        print(f"--> Número de colunas após remoção: {dados.shape[1]}")
    else:
        print("--> Não foram encontradas colunas vazias.")
    print('\n------Removendo Colunas Vazias------')
    return dados

# Sprint 3 - Limpeza dos dados - remover registros duplicados
def verificar_e_remover_duplicatas(dados):
    print('\n-----------Verificando Duplicatas--------------------')
    duplicatas = dados.duplicated().sum()
    print(f"--> Número total de registros: {dados.shape[0]}")
    print(f"--> Total de registros duplicados: {duplicatas}")
    if duplicatas > 0:
        print('--> Criando copia dos dados marcados como duplicados para análise...')
        dados_duplicados = dados[dados.duplicated(keep='first')]
        criar_arquivo_csv('backup/dados_duplicados.csv', dados_duplicados)
        print('--> Removendo registros duplicados...')
        dados_sem_duplicatas = dados.drop_duplicates()
        print(f"--> Número de registros após remoção de duplicatas: {dados_sem_duplicatas.shape[0]}")
        return dados_sem_duplicatas
    else:
        print("--> Não foram encontradas duplicatas.")
        return dados

# Sprint 3 - Limpeza dos dados - tratar valores nulos
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

# Sprint 3 - Limpeza dos dados - tratar valores discrepantes
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

# Fim das funções de limpeza dos dados

def executar_tarefas_de_transformacao(dados):
    transforma_campos_tipo_data(dados, 'DATA')
    verificar_limpar_strings(dados, ['CL_GENERO', 'CL_SEG','PR_CAT','PR_NOME'])
    verificar_limpar_inteiros(dados, ['CO_ID','CL_ID','CL_EC','CL_FHL','PR_ID'])
    apresentar_informacoes_dados(dados, "dados após a transformação")

def executar_tarefas_de_limpeza(dados):
    print("\n-> Iniciando tarefas de limpeza dos dados...")
    dados = remover_colunas_vazias(dados)
    dados = verificar_e_remover_duplicatas(dados)
    dados = verificar_e_tratar_valores_nulos(dados)
    dados = verificar_e_tratar_valores_discrepantes(dados)
    apresentar_informacoes_dados(dados, "dados após a limpeza")
    print("\n-> Tarefas de limpeza dos dados concluídas!")
    return dados

# Método de inicialização do programa
# Utilizado para chamar as funções de carregamento de dados, transformação e limpeza
def main():
    caminho_arquivo = 'database/base_varejo.csv'
    dados = carregar_dados_de_csv(caminho_arquivo)
    if dados is None:
        print("Falha ao carregar os dados.")
    else:
        print("-> Dados carregados com sucesso! Iniciando processos...")        
        apresentar_informacoes_dados(dados, "dados após o carregamento")
        dados = executar_tarefas_de_transformacao(dados)
        #dados = executar_tarefas_de_limpeza(dados)  

if __name__ == "__main__":
    main()