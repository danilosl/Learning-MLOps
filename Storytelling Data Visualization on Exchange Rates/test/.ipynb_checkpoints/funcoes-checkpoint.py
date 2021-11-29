'''
    Autor: Danilo de Sousa Lopes
    Data: nov/2021
    Criando um  conjunto de configurações para utilizarmos os testes em nosso problema
    proposto. Abaixo iremos definir algumas funções para realizar tais feitos.
'''
import logging
import pandas as pd

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
        dataframe = pd.read_csv(file_path)
        logging.info("SUCESSO: nenhum problema ao ler o arquivo!")
        return dataframe
    except: # pylint: disable=broad-except
        logging.error(
            "ERROR: não foi possível ler o arquivo %s",file_path)
        return None


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
        assert isinstance(janela, int)
        media_movel = coluna.rolling(janela).mean()
        logging.info("SUCESSO: O valor da janela é %s int",janela)
        return media_movel
    except: # pylint: disable=broad-except
        logging.error("ERROR: O valor da janela deve ser inteiro!")
        return None