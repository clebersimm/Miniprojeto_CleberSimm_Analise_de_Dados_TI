# Mini-projeto Avaliativo   

```
Análise de dados com Python [T1]
Mini-projeto avaliativo módulo 1 - semana 07
```

## Atividades  

Seguir as instruções do arquivo [Mini projeto](./mini_projeto.md).  


## Dicionário de dados    

- Data: data da compra.
- CO_ID: Identificação do número da compra (número da nota fiscal).   
- CL_ID: Identificação do cliente (número do cliente).   
- CL_GENERO: Sexo biológico informado pelo cliente.  
- CL_EC: Estado civil do cliente: 
    - 1: Casado ou união estável
    - 2: Divorciado
    - 3: Seprado
    - 4: Solteiro
    - 5: Viúvo
- CL_FHL: Número de filhos do cliente
- CL_SEG: Segmentação econômica do cliente (Classe A, B ou C)
- PR_ID: Código do produco (SKU) adquirido
- PR_CAT: Categoria do produto adquirido
- PR_NOME: Nome do produto adquirido


### Sprint 1 

Versão do python utilizada: Python 3.8.10   
Sistema Operacional: Ubuntu 20.04   

Sprint 1 (Importação dos dados): Realização da importação dos dados na plataforma Kaggle para a IDE VsCode ou Colab, onde  o script  será executado.

- [x] Criar estrutura do projeto
    - [x] Pasta database
    - [x] Pasta src
- [x] Download do arquivo indicado no documento de especificações do projeto. https://www.kaggle.com/datasets/namespaiva/base-varejo/data    
- [x] Descompactar a base de dados e normalizar o nome do arquivo de Base Varejo.csv para base_varejo.csv (removido arquivo .zip para não poluir)
- [x] Criar Virtual Environment
    - [x] python3 -m venv Miniprojeto
    - [x] source Miniprojeto/bin/active
    - [x] instalar pandas: pip3 install pandas
    - [x] freeze nas dependencias - aumentar a segurança contra chain attack: pip3 freeze > requirements.txt
    - [x] adicionado pasta Miniprojeto ao gitignore


## Sprint 2  

Sprint 2 (Transformação de Strings, Integer e Float e Datetime): Desenvolvimento das funções de limpeza de texto, inteiros e decimais usando métodos e expressões regulares.

- Divisão de responsábilidades dentro do arquivo, criando funções para carregar os dados

- [x] Criar função para carregar os dados do arquivo CSV, base de dados do sistema. 
- [x] Transformação dos dados
  - [x] Converter campo de data - Existe somente um campo do tipo de data, DATA, convertido para datetime
  - [x] Limpeza e transformação de strings - remoção dos espaços em branco e normalizando para uppercase
  - [x] Transformação dos inteiros - verificando se existe alguma dado nas colunas de inteiro que não seja número, se encontrado marcando como NaN
  - [ ] ~~Transformação dos decimais~~ não existem números decimais. Tarefa não será realizada.


## Sprint 3

- [ ] Funções para limpeza de dados
  - [x] Remoção de colunas inválidas - **remover_colunas_vazias**. Ao carregar os dados utilizando pandas, são apontadas 14 colunas mas a base só possui 10 colunas nas definições dedados. Removidas as colunas vazias.
  - [x] Remoção das registros duplicados - **verificar_e_remover_duplicatas**. Função que verifica os registros duplicados, após verificar se existem dados duplicados é realizada copia dos dados para futura análise e depois remoção dos dados.
  - [x] Verificação e remoção de dados nulos.
  - [ ] Tranformações de dados inválidos ou vazios.