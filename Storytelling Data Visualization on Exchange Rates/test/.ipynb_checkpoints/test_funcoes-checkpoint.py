'''
    Autor: Danilo de Sousa Lopes
    Data: nov/2021
    Caso o dataset já esteja na mesma pasta do arquivo basta chama-lo
    diretamente. Se você optou por clonar o repositório, passe o caminho
    completo do arquivo ou o link.
    Vale ressaltar que antes de realizar o teste é necessário fazer a
    limpeza de outliers do dataset e verificar o formato de dados das 
    colunas que serão utilizadas, sujeitas e conversão.
    
'''  
# importações necessárias
import pandas as pd
from funcoes import read_data
from funcoes import calc_rolling_mean  
FILE_PATH = 'euro-daily_test.csv'

def test_read_data():
    '''
        Teste da função read_data, utilizando o dataframe de teste.
    '''
    assert isinstance(read_data(FILE_PATH), pd.DataFrame)
    
def test_rolling_mean():
    '''
        Teste da função calc_rolling_mean, utilizando o dataframe de teste.
    '''
    assert isinstance(calc_rolling_mean(read_data('euro-daily_test.csv')['US_dollar'],30), pd.Series)
