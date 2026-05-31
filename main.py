# 1 - carregar os dados, mostrando número de registros, colunas e tipos de dados
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Constantes
DADOS_INVALIDOS = "DADOS_INVALIDOS"
ESTADO_CIVIL_VALIDO = {1:"Casado ou União Estável", 2:"Divorciado", 3:"Separado", 4:"Solteiro", 5:"Viúvo"}
NOME_BASE_DADOS_LIMPA = 'database/base_limpa.csv'

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
    total_registros_invalidos = 0
    for coluna in colunas:
        print(f'\n--> Verificando e Limpando Strings na coluna "{coluna}"')
        if coluna in dados.columns and dados[coluna].dtype == 'object':
            dados[coluna] = dados[coluna].astype(str).str.strip().str.upper()  # Remove espaços em branco e converte para maiúsculas
            # função que verifica se existem caracteres especiais na coluna e os remove
            # remove a linha inteira do dataframe e contabiliza os registros inválidos
            if dados[coluna].str.contains(r'[^\w\s]', regex=True).any():
                print(f"---> Atenção: A coluna '{coluna}' contém caracteres especiais. Removendo os registros inválidos.<---")
                total_invalidos = dados[coluna].str.contains(r'[^\w\s]', regex=True).sum()
                total_registros_invalidos += total_invalidos
                dados = dados[~dados[coluna].str.contains(r'[^\w\s]', regex=True)]
            print(f"--> Coluna '{coluna}' limpa com sucesso.")
        else:
            print(f"--> Coluna '{coluna}' não encontrada ou não é do tipo string.")
    print(f'\n------Fim da verificação e limpeza das colunas {colunas}------')
    return dados, total_registros_invalidos

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


# Sprint 4 (Estatística Descritiva)

# Analise da coluna número de filhos
def analise_coluna_numero_filhos(dados):
    print('\n------Análise da coluna número de filhos------')
    coluna_filho = 'CL_FHL'
    if coluna_filho not in dados.columns:
        print(f"--> Coluna '{coluna_filho}' não encontrada para análise.")
        return None
    #print(dados.groupby('CL_ID')[coluna_filho].value_counts()) - tratar estes dados de filho, pois não faz sentido
    #contador_filhos = dados[coluna_filho].count()
    media_filhos = dados[coluna_filho].mean()
    mediana_filhos = dados[coluna_filho].median()
    moda_filhos = dados[coluna_filho].mode()[0]
    minimo_filhos = dados[coluna_filho].min()
    maximo_filhos = dados[coluna_filho].max()
    quartil_25_filhos = dados[coluna_filho].quantile(0.25)
    quartil_75_filhos = dados[coluna_filho].quantile(0.75)
    analise_filhos = {
     #   "contador": contador_filhos,
        "media": media_filhos,
        "mediana": mediana_filhos,
        "moda": moda_filhos,
        "minimo": minimo_filhos,
        "maximo": maximo_filhos,
        "quartil_25": quartil_25_filhos,
        "quartil_75": quartil_75_filhos
    }
    
    return analise_filhos


# Sprint 4 - Estatística Descritiva
def analise_agrupamento_genero_categoria_compra(dados):
    print('--> Agrupamento de genero e categoria de compra')
    agrupado = dados.groupby(['CL_GENERO', 'PR_CAT']).size().reset_index(name='Quantidade_Comprada')
    tabela_pivot = agrupado.pivot(index='PR_CAT', columns='CL_GENERO', values='Quantidade_Comprada').fillna(0)
    fig, ax = plt.subplots(figsize=(10, 6))
    tabela_pivot.plot(kind='bar', ax=ax, width=0.8)
    plt.title('Quantidade Comprada por Categoria e Gênero', fontsize=14, pad=15)
    plt.xlabel('Categoria do Produto', fontsize=12)
    plt.ylabel('Quantidade Comprada', fontsize=12)
    plt.xticks(rotation=45, ha='right') 
    plt.legend(title='Gênero', labels=['Feminino (F)', 'Masculino (M)'])
    plt.tight_layout()
    plt.savefig('grafico_genero_categoria.png')
    return agrupado

def analise_agrupamento_itens_por_nota(dados):
    print('--> Agrupamento de itens por nota')
    itens_por_nota = dados.groupby('CO_ID').size().reset_index(name='Qtd_Itens')
    return itens_por_nota
    
def analise_agrupamento_top_produtos(dados):
    print('--> Agrupamento dos produtos mais comprados')
    top_produtos = dados.groupby('PR_NOME').size().reset_index(name='Quantidade')
    top_10 = top_produtos.sort_values(by='Quantidade', ascending=False).head(10)
    return top_10


def executar_tarefas_de_transformacao(dados):
    resultado_transformacao = []
    print('\n------Iniciando tarefas de transformação dos dados------')
    dados = transforma_campos_tipo_data(dados, 'DATA')
    dados, total_registros_invalidos = verificar_limpar_strings(dados, ['CL_GENERO', 'CL_SEG','PR_CAT','PR_NOME'])
    resultado_transformacao.append(f"Total de registros com strings inválidas removidos: {total_registros_invalidos}")
    dados, total_registros_alterados = verificar_limpar_inteiros(dados, ['CO_ID','CL_ID','CL_EC','CL_FHL','PR_ID'])
    resultado_transformacao.append(f"Total de registros com valores não numéricos marcados como NaN: {total_registros_alterados}")
    print("\n------Tarefas de transformação dos dados concluídas!------")
    return dados, resultado_transformacao

def executar_tarefas_de_limpeza(dados):
    resultado_limpeza = []
    print("\n-> Iniciando tarefas de limpeza dos dados...")
    dados, colunas_vazias = remover_colunas_vazias(dados)
    resultado_limpeza.append(f"Colunas vazias removidas: {list(colunas_vazias)}")
    dados, duplicatas = verificar_e_remover_duplicatas(dados)
    resultado_limpeza.append(f"Total de registros duplicados removidos: {duplicatas}")
    dados, total_nulos = verificar_e_tratar_valores_nulos(dados)
    resultado_limpeza.append(f"Total de dados nulos após tratamento: {total_nulos}")
    # Verificação de campos específicos
    # limpezas específicas de campos serão realizadas em outro momento. Necessário adquirir mais conhecimento sobre python
    #dados = verificar_e_tratar_campo_estado_civil(dados)
    #dados = verificar_e_tratar_valores_discrepantes(dados)
    print("\n-> Tarefas de limpeza dos dados concluídas!")
    return dados, resultado_limpeza

def executar_tarefas_analise():
    resultado_analise = []
    print("\n-> Iniciando tarefas de análise dos dados...")
    dados_limpos = carregar_dados_de_csv(NOME_BASE_DADOS_LIMPA)
    resultado_analise_coluna_filhos = analise_coluna_numero_filhos(dados_limpos)
    resultado_analise.append(f"Resultado da análise da coluna número de filhos: {resultado_analise_coluna_filhos}")
    resultado_genero_categoria_compra = analise_agrupamento_genero_categoria_compra(dados_limpos)
    resultado_analise.append(f"Resultado do agrupamento de gênero e categoria de compra: {resultado_genero_categoria_compra}")
    resultado_itens_por_nota = analise_agrupamento_itens_por_nota(dados_limpos)
    resultado_analise.append(f"Resultado do agrupamento de itens por nota: {resultado_itens_por_nota}")
    resultado_top_produtos = analise_agrupamento_top_produtos(dados_limpos)
    resultado_analise.append(f"Resultado do agrupamento dos produtos mais comprados: {resultado_top_produtos}")
    print("\n-> Tarefas de análise dos dados concluídas!")
    return resultado_analise,dados_limpos
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
        dados, resultado_transformacao = executar_tarefas_de_transformacao(dados)
        apresentar_informacoes_dados(dados, "dados após a transformação")
        dados, resultado_limpeza = executar_tarefas_de_limpeza(dados)
        apresentar_informacoes_dados(dados, "dados após a limpeza")
        criar_arquivo_csv(NOME_BASE_DADOS_LIMPA, dados)
        del dados
        resultado_analise, dados_limpos = executar_tarefas_analise()
        print('\n------Sumário da execução do programa------')
        print('-> O programa realizou as seguintes etapas:')
        print('1. Carregamento dos dados do arquivo CSV.')
        print('2. Apresentação das informações dos dados após o carregamento.')
        print('3. Transformação dos dados, incluindo:')
        print('   - Transformação da coluna "DATA" para tipo datetime.')
        print('   - Verificação e limpeza das colunas "CL_GENERO", "CL_SEG", "PR_CAT" e "PR_NOME" de espaços em branco e caracteres especiais, convertendo para maiúsculas.')
        print('   - Verificação e limpeza das colunas "CO_ID", "CL_ID", "CL_EC", "CL_FHL" e "PR_ID" de valores não numéricos, marcando como NaN quando encontrados.')
        print('4. Apresentação das informações dos dados após a transformação.')
        print('5. Limpeza dos dados, incluindo:')
        print('   - Remoção de colunas vazias.')
        print('   - Verificação e remoção de registros duplicados, com backup dos dados duplicados para análise.')
        print('   - Verificação e tratamento de valores nulos, substituindo strings vazias e valores "NULL" por NaN.')
        print('6. Apresentação das informações dos dados após a limpeza.')
        print('7. Criação de um novo arquivo CSV com os dados limpos.')
        print('8. Análise dos dados limpos, incluindo:')
        print('   - Análise da coluna número de filhos, calculando média, mediana, moda, mínimo, máximo e quartis.')
        print('   - Agrupamento de gênero e categoria de compra, com visualização em gráfico de barras.')
        print('   - Agrupamento de itens por nota, com estatísticas descritivas.')
        print('   - Agrupamento dos produtos mais comprados, com identificação do top 10 produtos.')
        print('-> O programa foi executado com sucesso, realizando todas as etapas de carregamento, transformação, limpeza e análise dos dados, fornecendo insights valiosos sobre o comportamento de compra dos clientes.')
        print('\n--> Insights obtidos durante a execução do programa:')
        print('-> Durante a transformação dos dados:')
        for insight in resultado_transformacao:
            print(f'   - {insight}')
        print('-> Durante a limpeza dos dados:')
        for insight in resultado_limpeza:
            print(f'   - {insight}')
        print('\n-> Resultado da limpeza dos dados limpos:')
        apresentar_informacoes_dados(dados_limpos, "dados limpos para análise")
        print('\n-> Resultado da análise dos dados limpos:')
        for insight in resultado_analise:
            print(f'   - {insight}')

if __name__ == "__main__":
    main()