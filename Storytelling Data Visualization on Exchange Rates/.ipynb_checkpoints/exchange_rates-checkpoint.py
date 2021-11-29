
'''
    Autor: Danilo de Sousa Lopes
    Data: nov/2021
    Esse é o exchange_rates.py da solução do projeto guiado Storytelling Data Visualization
    on Exchange Rates caso queria mais detalhes do desenvolvimento, verifique o notebook
    exchange_rates.ipynb
    Criando um  conjunto de configurações para utilizarmos os testes em nosso problema
    proposto. Abaixo iremos definir algumas funções para realizar tais feitos.
'''

# importando as bibliotecas necessárias
import logging
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.style as style

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


# Leitura e Análise do Conjunto de Dados
# lendo o dataframe .csv
# pylint: disable=no-member
exchange_rates = read_data('euro-daily-hist_1999_2021.csv')

# Limpeza dos Dados
# renomear as colunas [US dollar ], [Brazilian real ] e Period\Unit:
exchange_rates.rename(columns={'[US dollar ]': 'US_dollar',
                               '[Brazilian real ]': 'Euro',
                               'Period\\Unit:': 'Time'},
                      inplace=True)

# mudar o tipo de dados da coluna Time para datetime
exchange_rates['Time'] = pd.to_datetime(exchange_rates['Time'])

# classificar os valores de Time em ordem crescente
exchange_rates.sort_values('Time', inplace=True)

# reinicializar os índices e eliminar o índice inicial
exchange_rates.reset_index(drop=True, inplace=True)

# separa as colunas Time, Euro e Dollar para atribuir ao novo dataframe
# exchange_rates_to_real
# pylint: disable=E1136 
exchange_rates_to_real = exchange_rates[['Time', 'Euro', 'US_dollar']].copy()

# separados os valores que não possuem '-'.
exchange_rates_to_real = exchange_rates_to_real[exchange_rates_to_real['Euro'] != '-']
exchange_rates_to_real = exchange_rates_to_real[exchange_rates_to_real['US_dollar'] != '-']

# removendo os valores nulos
exchange_rates_to_real = exchange_rates_to_real.dropna()

# convertendo a coluna Euro e US_dollar para float
exchange_rates_to_real['Euro'] = exchange_rates_to_real['Euro'].astype(float)
exchange_rates_to_real['US_dollar'] = exchange_rates_to_real['US_dollar'].astype(
    float)
exchange_rates_to_real['US_dollar'] = exchange_rates_to_real['Euro'] / \
    exchange_rates_to_real['US_dollar']

# Análise Gráfica
# gerando um gráfico de linhas para visualizar a evolução da taxa de
# câmbio euro-real e dólar_real
plt.plot(exchange_rates_to_real['Time'], exchange_rates_to_real['Euro'], c='g')
plt.plot(exchange_rates_to_real['Time'], exchange_rates_to_real['US_dollar'])
plt.show()

# Média Móvel
# Euro
# definindo as propriedades pra figura
plt.figure(figsize=(9, 6))
plt.subplot(3, 2, 1)
plt.plot(exchange_rates_to_real['Time'], exchange_rates_to_real['Euro'])
plt.title('Valores Originais', weight='bold')
for i, rolling_mean in zip([2, 3, 4, 5, 6],
                           [7, 30, 50, 100, 365]):
    plt.subplot(3, 2, i)
    plt.plot(exchange_rates_to_real['Time'],
             exchange_rates_to_real['Euro'].rolling(rolling_mean).mean())
    plt.title('Janela Móvel: ' + str(rolling_mean) + ' dias', weight='bold')

# ajusta automaticamente o preechimento entre os subplots
plt.tight_layout()
plt.show()

# Dólar
# definindo as propriedades pra figura
plt.figure(figsize=(9, 6))
plt.subplot(3, 2, 1)
plt.plot(exchange_rates_to_real['Time'], exchange_rates_to_real['US_dollar'])
plt.title('Valores Originais', weight='bold')
for i, rolling_mean in zip([2, 3, 4, 5, 6],
                           [7, 30, 50, 100, 365]):
    plt.subplot(3, 2, i)
    plt.plot(exchange_rates_to_real['Time'],
             exchange_rates_to_real['US_dollar'].rolling(rolling_mean).mean())
    plt.title('Janela Móvel: ' + str(rolling_mean) + ' dias', weight='bold')

# ajusta automaticamente o preechimento entre os subplots
plt.tight_layout()
plt.show()

# definindo a janela móvel de 30 dias para utilizarmos.
exchange_rates_to_real['rolling_mean_euro'] = calc_rolling_mean(
    exchange_rates_to_real['Euro'], 30)
exchange_rates_to_real['rolling_mean_dollar'] = calc_rolling_mean(
    exchange_rates_to_real['US_dollar'], 30)

# análise gráfica
plt.plot(
    exchange_rates_to_real['Time'],
    exchange_rates_to_real['rolling_mean_euro'],
    c='g')
plt.plot(exchange_rates_to_real['Time'],
         exchange_rates_to_real['rolling_mean_dollar'])
plt.show()

# Análise das Taxas de Câmbio do Real em relação ao Euro durante 
# os Governos Brasileiros entre os anos 2000 e 2021.
# separando as taxas de câmbio do real x euro por governos.
fhc = exchange_rates_to_real.copy()[
    exchange_rates_to_real['Time'].dt.year < 2003]
lula = exchange_rates_to_real.copy()[
    (exchange_rates_to_real['Time'].dt.year >= 2003) & (
        exchange_rates_to_real['Time'].dt.year < 2011)]
dilma = exchange_rates_to_real.copy()[
    (exchange_rates_to_real['Time'].dt.year >= 2011) & (
        exchange_rates_to_real['Time'] < '2016-08-31')]
temer = exchange_rates_to_real.copy()[
    (exchange_rates_to_real['Time'] >= '2016-08-31') & (
        exchange_rates_to_real['Time'].dt.year < 2019)]
bolsonaro = exchange_rates_to_real.copy()[
    (exchange_rates_to_real['Time'].dt.year >= 2019)]

# Gerando o gráfico utilizando o style Fivethirtyeight
# adicionando o style
style.use('fivethirtyeight')

# adicionando os subplots
plt.figure(figsize=(18, 8))
ax1 = plt.subplot(2, 5, 1)
ax2 = plt.subplot(2, 5, 2)
ax3 = plt.subplot(2, 5, 3)
ax4 = plt.subplot(2, 5, 4)
ax5 = plt.subplot(2, 5, 5)
ax6 = plt.subplot(2, 1, 2)
axes = [ax1, ax2, ax3, ax4, ax5, ax6]

# fazendo alterações e adicionando as legendas aos gráficos
for ax in axes:
    ax.set_ylim(0.5, 2.0)
    ax.set_yticks([2.0, 3.0, 4.0, 5.0, 6.0, 7.0])
    ax.set_yticklabels(['2.0', '3.0', '4.0', '5.0', '6.0', '7.0'],
                       alpha=0.3)
    ax.set_xticklabels([])
    ax.grid(alpha=0.5)

# gráfico ax1: fhc
ax1.plot(fhc['Time'], fhc['rolling_mean_euro'], color='#BF5FFF')
ax1.set_xticklabels(['', '2000', '', '', '2001',
                    '', '', '2002', ''], alpha=0.3)
ax1.text(730576.0, 8.0, 'FHC', fontsize=18, weight='bold', color='#BF5FFF')
ax1.text(730380.0, 7.5, '(2000-2002)', weight='bold', alpha=0.3)

# gráfico ax2: lula
ax2.plot(lula['Time'], lula['rolling_mean_euro'], color='#ffa500')
ax2.set_xticklabels(['', '2002', '', '2004', '', '2006', '',
                     '2008', '', '2010'],
                    alpha=0.3)
ax2.text(732288.0, 8.0, 'LULA', fontsize=18, weight='bold', color='#ffa500')
ax2.text(731900.0, 7.5, '(2003-2010)', weight='bold', alpha=0.3)

# gráfico ax3: dilma
ax3.plot(dilma['Time'], dilma['rolling_mean_euro'], color='#00B2EE')
ax3.set_xticklabels(
    ['', '2011', '', '        2014', '', '', '2016'], alpha=0.3)
ax3.text(734705.0, 8.0, 'DILMA', fontsize=18, weight='bold', color='#00B2EE')
ax3.text(734518.0, 7.5, '(2011-2016)', weight='bold', alpha=0.3)

# gráfico ax4: temer
ax4.plot(temer['Time'], temer['rolling_mean_euro'], color='g')
ax4.set_xticklabels(['2016', '', '', '', '2017',
                    '', '', '', '2018'], alpha=0.3)
ax4.text(736460.0, 8.0, 'TEMER', fontsize=18, weight='bold', color='g')
ax4.text(736400.0, 7.5, '(2016-2018)', weight='bold', alpha=0.3)

# gráfico ax5: bolsonaro
ax5.plot(bolsonaro['Time'], bolsonaro['rolling_mean_euro'], color='b')
ax5.set_xticklabels(['', '2019', '', '', '2020',
                    '', '', '2021', ''], alpha=0.3)
ax5.text(737185.0, 8.0, 'BOLSONARO', fontsize=18, weight='bold', color='b')
ax5.text(737230.0, 7.5, '(2019-ATUAL)', weight='bold', alpha=0.3)

# gráfico dos presidentes
ax6.plot(fhc['Time'], fhc['rolling_mean_euro'], color='#BF5FFF')
ax6.plot(lula['Time'], lula['rolling_mean_euro'], color='#ffa500')
ax6.plot(dilma['Time'], dilma['rolling_mean_euro'], color='#00B2EE')
ax6.plot(temer['Time'], temer['rolling_mean_euro'], color='g')
ax6.plot(bolsonaro['Time'], bolsonaro['rolling_mean_euro'], color='b')
ax6.grid(alpha=0.5)
ax6.set_xticks([])

# título e subtitulo do gráfico
ax1.text(730016.0, 10.1, 'TAXA DE CÂMBIO EURO-REAL ENTRE 2000-2021',
         fontsize=20, weight='bold')
ax1.text(730016.0, 8.9, '''Taxas de câmbio EURO-REAL para os governos:
FHC (2000 - 2002), Lula (2003 - 2010), Dilma (2011-2016), 
Temer (2016-2018), Bolsonaro (2019-ATUAL).''', fontsize=16)

# adicionando assinatura
ax6.text(729916.0, 0.65, 'DCA0305' + ' ' * 195 + 'Danilo de Sousa Lopes',
         color='#f0f0f0', backgroundcolor='#4d4d4d', size=14)
plt.savefig("euro_to_real.png")


# Análise das Taxas de Câmbio do Real em relação ao Dólar durante os 
# Governos Brasileiros entre os anos 2000 e 2021.
# adicionando os subplots
plt.figure(figsize=(18, 8))
ax1 = plt.subplot(2, 5, 1)
ax2 = plt.subplot(2, 5, 2)
ax3 = plt.subplot(2, 5, 3)
ax4 = plt.subplot(2, 5, 4)
ax5 = plt.subplot(2, 5, 5)
ax6 = plt.subplot(2, 1, 2)
axes = [ax1, ax2, ax3, ax4, ax5, ax6]

# fazendo alterações e adicionando as legendas aos gráficos
for ax in axes:
    ax.set_ylim(0.5, 2.0)
    ax.set_yticks([1.0, 2.0, 3.0, 4.0, 5.0, 6.0])
    ax.set_yticklabels(['1.0', '2.0', '3.0', '4.0', '5.0', '6.0'],
                       alpha=0.3)
    ax.set_xticklabels([])
    ax.grid(alpha=0.5)

# gráfico ax1: fhc
ax1.plot(fhc['Time'], fhc['rolling_mean_dollar'], color='#BF5FFF')
ax1.set_xticklabels(['', '2000', '', '', '2001',
                    '', '', '2002', ''], alpha=0.3)
ax1.text(730576.0, 7.0, 'FHC', fontsize=18, weight='bold', color='#BF5FFF')
ax1.text(730380.0, 6.5, '(2000-2002)', weight='bold', alpha=0.3)

# gráfico ax2: lula
ax2.plot(lula['Time'], lula['rolling_mean_dollar'], color='#ffa500')
ax2.set_xticklabels(['', '2002', '', '2004', '', '2006', '',
                     '2008', '', '2010'],
                    alpha=0.3)
ax2.text(732288.0, 7.0, 'LULA', fontsize=18, weight='bold', color='#ffa500')
ax2.text(731900.0, 6.5, '(2003-2010)', weight='bold', alpha=0.3)

# gráfico ax3: dilma
ax3.plot(dilma['Time'], dilma['rolling_mean_dollar'], color='#00B2EE')
ax3.set_xticklabels(
    ['', '2011', '', '        2014', '', '', '2016'], alpha=0.3)
ax3.text(734705.0, 7.0, 'DILMA', fontsize=18, weight='bold', color='#00B2EE')
ax3.text(734518.0, 6.5, '(2011-2016)', weight='bold', alpha=0.3)

# gráfico ax4: temer
ax4.plot(temer['Time'], temer['rolling_mean_dollar'], color='g')
ax4.set_xticklabels(['2016', '', '', '', '2017',
                    '', '', '', '2018'], alpha=0.3)
ax4.text(736460.0, 7.0, 'TEMER', fontsize=18, weight='bold', color='g')
ax4.text(736400.0, 6.5, '(2016-2018)', weight='bold', alpha=0.3)

# gráfico ax5: bolsonaro
ax5.plot(bolsonaro['Time'], bolsonaro['rolling_mean_dollar'], color='b')
ax5.set_xticklabels(['', '2019', '', '', '2020',
                    '', '', '2021', ''], alpha=0.3)
ax5.text(737185.0, 7.0, 'BOLSONARO', fontsize=18, weight='bold', color='b')
ax5.text(737230.0, 6.5, '(2019-ATUAL)', weight='bold', alpha=0.3)

# gráfico dos presidentes
ax6.plot(fhc['Time'], fhc['rolling_mean_dollar'], color='#BF5FFF')
ax6.plot(lula['Time'], lula['rolling_mean_dollar'], color='#ffa500')
ax6.plot(dilma['Time'], dilma['rolling_mean_dollar'], color='#00B2EE')
ax6.plot(temer['Time'], temer['rolling_mean_dollar'], color='g')
ax6.plot(bolsonaro['Time'], bolsonaro['rolling_mean_dollar'], color='b')
ax6.grid(alpha=0.5)
ax6.set_xticks([])

# título e subtitulo do gráfico
ax1.text(730016.0, 8.9, 'TAXA DE CÂMBIO USD-REAL ENTRE 2000-2021',
         fontsize=20, weight='bold')
ax1.text(730016.0, 7.9, '''Taxas de câmbio USD-REAL para os governos:
FHC (2000 - 2002), Lula (2003 - 2010), Dilma (2011-2016), Temer (2016-2018), 
Bolsonaro (2019-ATUAL).''', fontsize=16)

# adicionando assinatura
ax6.text(729916.0, 0.65, 'DCA0305' + ' ' * 195 + 'Danilo de Sousa Lopes',
         color='#f0f0f0', backgroundcolor='#4d4d4d', size=14)
plt.savefig("dollar_to_real.png")


# Análise das Taxas de Câmbio do Real, contrastre entre os gráfios Euro x Real e Dólar x Real
# definindo as propriedades da figura
fig, (ax1, ax2) = plt.subplots(2, sharex=True, figsize=(16, 8))

# adicionando o título e subtitulo ao gráfico
ax1.text(729700.0, 8.9,
    'TAXA DE CÂMBIO EURO(€) x REAL(R$) E DÓLAR(US$) x REAL(R$) ENTRE 2000-2021',
    fontsize=20, weight='bold')
ax1.text(729700.0, 7.9, '''Taxas de câmbio do REAL para os governos: 
FHC (2000 - 2002), Lula (2003 - 2010), Dilma (2011-2016), Temer (2016-2018),
Bolsonaro (2019-ATUAL).''', fontsize=16)

# gráfico real x euro
ax1.plot(fhc['Time'], fhc['rolling_mean_euro'], color='#BF5FFF', label="FHC")
ax1.plot(
    lula['Time'],
    lula['rolling_mean_euro'],
    color='#ffa500',
    label="Lula")
ax1.plot(
    dilma['Time'],
    dilma['rolling_mean_euro'],
    color='#00B2EE',
    label="Dilma")
ax1.plot(temer['Time'], temer['rolling_mean_euro'], color='g', label="Temer")
ax1.plot(
    bolsonaro['Time'],
    bolsonaro['rolling_mean_euro'],
    color='b',
    label="Bolsonaro")
ax1.set_title('EUR x BRL')
ax1.grid(alpha=0.5)
ax1.legend()

# gráfico real x dólar
ax2.plot(fhc['Time'], fhc['rolling_mean_dollar'], color='#BF5FFF')
ax2.plot(lula['Time'], lula['rolling_mean_dollar'], color='#ffa500')
ax2.plot(dilma['Time'], dilma['rolling_mean_dollar'], color='#00B2EE')
ax2.plot(temer['Time'], temer['rolling_mean_dollar'], color='g')
ax2.plot(bolsonaro['Time'], bolsonaro['rolling_mean_dollar'], color='b')
ax2.set_title('USD x BRL')
ax2.grid(alpha=0.5)

# adicionando assinatura
ax2.text(729700.0, 0.33, 'DCA0305' + ' ' * 187 + 'Danilo de Sousa Lopes',
         color='#f0f0f0', backgroundcolor='#4d4d4d', size=14)
plt.savefig("euro_dollar_to_real.png")
plt.tight_layout()
plt.subplots_adjust(top=0.8, wspace=0.3)
plt.show()