# 1 - carregar os dados, mostrando número de registros, colunas e tipos de dados
import pandas as pd
import numpy as np

# Constantes
DADOS_INVALIDOS = "DADOS_INVALIDOS"
ESTADO_CIVIL_VALIDO = {1:"Casado ou União Estável", 2:"Divorciado", 3:"Separado", 4:"Solteiro", 5:"Viúvo"}

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
    print("--> Amostra dos dados:")
    print(dados.head())
    print("--> Valores nulos por coluna:")
    print(dados.isnull().sum())
    print('------Fim informações dos dados------\n')

# Fim das Funções utilitárias

## Inicio das funções de transformação dos dados

# Sprint 2 - Transformação dos dados - transformar campos de data para tipo datetime
def transforma_campos_tipo_data(dados, coluna):
    print(f'\n------Transformação da coluna "{coluna}" para tipo datetime------')
    dados[coluna] = pd.to_datetime(dados[coluna], dayfirst=True, errors='coerce')
    print(f"--> Coluna '{coluna}' transformada para tipo datetime com sucesso.")
    print(f'------Fim da transformação da coluna "{coluna}" para tipo datetime------\n')
    return dados

# Sprint 2 - Transformação dos dados - verificar e limpar strings (remover espaços em branco, caracteres especiais, etc.)
def verificar_limpar_strings(dados, colunas):
    print(f'\n------Verificando as colunas {colunas}, são valores string,para limpeza e normalização dos dados------')
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
    total_registros_alterados = 0
    for coluna in colunas:
        print(f'\n--> Verificando e Limpando Inteiros na coluna "{coluna}"')
        if coluna in dados.columns:
            # Verifica se existem valores não numéricos usando regex \D (qualquer caractere que não seja dígito)
            if dados[coluna].astype(str).str.contains(r'\D', regex=True).any():
                print(f"---> Atenção: A coluna '{coluna}' contém valores não numéricos. Marcando os dados inválidos.<---")
                dados[coluna] = dados[coluna].astype(str).str.replace(r'\D', 'NaN', regex=True)
                total_registros_alterados += dados[coluna].str.contains('NaN').sum()
            else:
                print(f"--> Coluna '{coluna}' contém apenas números.")
            print(f"--> Coluna '{coluna}' verificada e limpa com sucesso.")
        else:
            print(f"--> Coluna '{coluna}' não encontrada.")
    print(f'\n------Fim da verificação e limpeza das colunas {colunas}------')
    return dados, total_registros_alterados

# Fim das funções de transformação dos dados


# Inicio das funções de limpeza dos dados

# Sprint 3 - Limpeza dos dados. Foram identificadas colunas vazias, não possuindo informações. Desta forma sendo removidas
def remover_colunas_vazias(dados):
    print('\n------Removendo Colunas Vazias------')
    colunas_vazias = dados.columns[dados.isnull().all()]
    if len(colunas_vazias) > 0:
        print(f"--> Colunas vazias encontradas. Total: {len(colunas_vazias)}, nomes: {list(colunas_vazias)}")
        dados = dados.drop(columns=colunas_vazias)
        print(f"--> Número de colunas após remoção: {dados.shape[1]}")
    else:
        print("--> Não foram encontradas colunas vazias.")
    print('\n------Fim da remoção de colunas vazias------')
    return dados, colunas_vazias

# Sprint 3 - Limpeza dos dados - remover registros duplicados
def verificar_e_remover_duplicatas(dados):
    print('\n------Verificando Duplicatas------')
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
        return dados_sem_duplicatas, duplicatas
    else:
        print("--> Não foram encontradas duplicatas.")
        return dados, duplicatas

# Sprint 3 - Limpeza dos dados - tratar valores nulos
def verificar_e_tratar_valores_nulos(dados):
    print('\n------Verificando Valores Nulos------')
    total_nulos = dados.isnull().sum()
    print(f'--> Total dados nulos: {total_nulos}')
    print('--> Verificando se existem strings vazias e NULL')
    dados = dados.replace({'NULL':np.nan, 'N/A':np.nan, '':np.nan})
    total_nulos = dados.isnull().sum()
    print(f'--> Total dados nulos após substituição: {total_nulos}')
    print('\n------Fim da verificação e tratamento de valores nulos------')
    # Resetando o índice após a limpeza dos dados
    dados = dados.reset_index(drop=True)
    return dados, total_nulos

# Sprint 3 - Limpeza dos dados - estado_civil
def verificar_e_tratar_campo_estado_civil(dados):
    print('\n------Verificando Valores do estado civil------')
    print('--> Campo estado civil somente pode possuir os valores 1(casado ou união estável), 2(divorciado), 3(separado), 4(solteiro) e 5(viúvo).')
    expressao_verificar_estado_civil_valido = r'^[1-5]$'
    if dados['CL_EC'].astype(str).str.contains(expressao_verificar_estado_civil_valido, regex=True).all():
        print("--> Todos os registros do campo estado civil estão válidos.")
    else:
        print("---> Atenção: Foram encontrados registros com valores inválidos no campo estado civil. Marcando os dados inválidos.<---")
        dados['CL_EC'] = dados['CL_EC'].astype(str).str.replace(r'[^1-5]', 0, regex=True)
    print('\n------Fim da verificação e tratamento do campo estado civil------')
    return dados

# Sprint 3 - Limpeza dos dados - categoria
def verificar_e_tratar_campo_marcados_como_invalidos(dados):
    print('\n------Verificando Valores do campo marcados como inválidos------')
    

# Fim das funções de limpeza dos dados

def executar_tarefas_de_transformacao(dados):
    print("\n-> Iniciando tarefas de transformação dos dados...")
    dados = transforma_campos_tipo_data(dados, 'DATA')
    dados = verificar_limpar_strings(dados, ['CL_GENERO', 'CL_SEG','PR_CAT','PR_NOME'])
    dados, total_registros_alterados = verificar_limpar_inteiros(dados, ['CO_ID','CL_ID','CL_EC','CL_FHL','PR_ID'])
    print("\n-> Tarefas de transformação dos dados concluídas!")
    print('-----Sumário da execução das tarefas de transformação dos dados-----')
    print('-> Coluna "DATA" transformada para tipo datetime.')
    print('-> Colunas "CL_GENERO", "CL_SEG", "PR_CAT" e "PR_NOME" limpas de espaços em branco e caracteres especiais, convertidas para maiúsculas.')
    print('-> Colunas "CO_ID", "CL_ID", "CL_EC", "CL_FHL" e "PR_ID" verificadas e limpas de valores não numéricos, marcados como NaN quando encontrados.')
    print(f'-> Total de registros alterados durante a verificação e limpeza de inteiros: {total_registros_alterados}')
    print('--------------------------------------------------------------------')
    return dados

def executar_tarefas_de_limpeza(dados):
    print("\n-> Iniciando tarefas de limpeza dos dados...")
    dados, colunas_vazias = remover_colunas_vazias(dados)
    dados, duplicatas = verificar_e_remover_duplicatas(dados)
    dados, total_nulos = verificar_e_tratar_valores_nulos(dados)
    # Verificação de campos específicos
    # deixar para depois
    #dados = verificar_e_tratar_campo_estado_civil(dados)
    #dados = verificar_e_tratar_valores_discrepantes(dados)
    #print("\n-> Tarefas de limpeza dos dados concluídas!")
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
        apresentar_informacoes_dados(dados, "dados após a transformação")
        dados = executar_tarefas_de_limpeza(dados)  
        #apresentar_informacoes_dados(dados, "dados após a limpeza")

if __name__ == "__main__":
    main()