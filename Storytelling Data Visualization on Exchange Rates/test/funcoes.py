'''
    Autor: Danilo de Sousa Lopes
    Data: nov/2021
    Criando um  conjunto de configurações para utilizarmos os testes em nosso problema
    proposto. Abaixo iremos definir algumas funções para realizar tais feitos.
'''
import pandas as pd
import logging

# definições do logging
logging.basicConfig(
    filename='test_results.log',
    level=logging.INFO,
    filemode='w',
    format='%(name)s - %(levelname)s - %(message)s')

def read_data(file_path):
    '''
    Função para a ler e verificar o dataframe.csv
    Args:
        file_path (str): arquivo para leitura.
    Return:
        df (Dataframe): retorna o arquivo lido no formato de dataframe.
    '''
    try:
        df = pd.read_csv(file_path)
        logging.info("SUCESSO: nenhum problema ao ler o arquivo!")
        return df
    except:
        logging.error("ERROR: não foi possível ler o arquivo {}".format(file_path))

def calc_rolling_mean(coluna, janela):
    '''
    Função para calcular média móvel dos valores distribuidos em uma coluna
    do dataframe, relação a uma janela temporal.
    Args:
        coluna (str): a coluna que contem a distribuição dos dados.
        janela (int): a janela móvel desejada (7 dias, 30 dias...).
    Return:
        rolling_mean (pandas Series): Serie com as médias móveis.
    '''
    try:
        assert(isinstance(janela, int))
        rolling_mean = coluna.rolling(janela).mean()
        logging.info("SUCESSO: O valor da janela é {} int".format(janela))
        return rolling_mean
    except:
        logging.error("ERROR: O valor da janela deve ser inteiro!")
