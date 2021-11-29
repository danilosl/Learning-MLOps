# importações necessárias
import pandas as pd
from funcoes import read_data
from funcoes import calc_rolling_mean

'''
    Caso o dataset ja esteja na mesma pasta do arquivo basta chama-lo
    diretamente. Se você optou por clonar o repositório, passe o caminho
    completo do arquivo ou o link:
    
'''    
file_path = 'euro-daily_test.csv'

def test_read_data():
    assert(isinstance(read_data(file_path), pd.DataFrame))
    
def test_rolling_mean():
    assert(isinstance(calc_rolling_mean(read_data('euro-daily_test.csv')['US_dollar'],30), pd.Series))
