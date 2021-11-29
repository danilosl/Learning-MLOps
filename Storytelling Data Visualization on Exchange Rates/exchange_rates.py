#!/usr/bin/env python
# coding: utf-8

# ## Storytelling Data Visualization on Exchange Rates
# Autor: Danilo de Sousa Lopes
# 
# Ao desenvolver o projeto guiado a seguir busca-se:
#  - Usar os prícipios do design de informação (familiaridade e maximização da proporção dados/tinta)
#  - Como criar visualizações de dados narrativos usando Matplotlib
#  - Como criar padrões visuais usando os princípios da Gestalt
#  - Como orientar a atenção do público com atributos pré-atenciosos.
#  - Como usar os estilos integrados do Matplotlib: com um estudo de caso sobre o estilo FiveThirtyEight.
# 
# Iremos combinar essas habilidades, trabalhando com o conjunto de dados reunido por Daria Chemkaeva e disponibilizado no Kaggle, que descreve as taxas de câmbio diárias de diversas moedas entre 1999 e 2020. Nosso objeto de estudo será as taxas de câmbio do Real e do Dólar, em relação ao Euro, entre os Governos FHC e Bolsonaro, para a moeda brasileira e entre os Governos Bush e Biden, para a moeda americana.            

# ### Teste & Logging

# In[113]:


get_ipython().run_cell_magic('file', 'funcoes.py', '\'\'\'\n    Autor: Danilo de Sousa Lopes\n    Data: nov/2021\n    Criando um  conjunto de configurações para utilizarmos os testes em nosso problema\n    proposto. Abaixo iremos definir algumas funções para realizar tais feitos.\n\'\'\'\nimport pandas as pd\nimport logging\n\n# definições do logging\nlogging.basicConfig(\n    filename=\'test_results.log\',\n    level=logging.INFO,\n    filemode=\'w\',\n    format=\'%(name)s - %(levelname)s - %(message)s\')\n\ndef read_data(file_path):\n    \'\'\'\n    Função para a ler e verificar o dataframe.csv\n    Args:\n        file_path (str): arquivo para leitura.\n    Return:\n        df (Dataframe): retorna o arquivo lido no formato de dataframe.\n    \'\'\'\n    try:\n        df = pd.read_csv(file_path)\n        logging.info("SUCESSO: nenhum problema ao ler o arquivo!")\n        return df\n    except:\n        logging.error("ERROR: não foi possível ler o arquivo {}".format(file_path))\n\ndef calc_rolling_mean(coluna, janela):\n    \'\'\'\n    Função para calcular média móvel dos valores distribuidos em uma coluna\n    do dataframe, relação a uma janela temporal.\n    Args:\n        coluna (str): a coluna que contem a distribuição dos dados.\n        janela (int): a janela móvel desejada (7 dias, 30 dias...).\n    Return:\n        rolling_mean (pandas Series): Serie com as médias móveis.\n    \'\'\'\n    try:\n        assert(isinstance(janela, int))\n        rolling_mean = coluna.rolling(janela).mean()\n        logging.info("SUCESSO: O valor da janela é {} int".format(janela))\n        return rolling_mean\n    except:\n        logging.error("ERROR: O valor da janela deve ser inteiro!")')


# In[114]:


get_ipython().run_cell_magic('file', 'test_funcoes.py', "# importações necessárias\nimport pandas as pd\nfrom funcoes import read_data\nfrom funcoes import calc_rolling_mean\n\n'''\n    Caso o dataset ja esteja na mesma pasta do arquivo basta chama-lo\n    diretamente. Se você optou por clonar o repositório, passe o caminho\n    completo do arquivo ou o link:\n    \n'''    \nfile_path = 'euro-daily_test.csv'\n\ndef test_read_data():\n    assert(isinstance(read_data(file_path), pd.DataFrame))\n    \ndef test_rolling_mean():\n    assert(isinstance(calc_rolling_mean(read_data('euro-daily_test.csv')['US_dollar'],30), pd.Series))")


# In[52]:


get_ipython().system('pip -q install pytest pytest-sugar')


# In[108]:


get_ipython().system('python -m pytest test_funcoes.py')


# ### Leitura e Análise do Conjunto de Dados

# In[116]:


# importanto as bibliotecas necessárias
import pandas as pd
import matplotlib.pyplot as plt
from funcoes import read_data
from funcoes import calc_rolling_mean

# comando mágio para permitir a exibição dos gráficos na célula
get_ipython().run_line_magic('matplotlib', 'inline')

# lendo o dataframe .csv
exchange_rates = read_data('euro-daily-hist_1999_2021.csv')

# verificando as primeiras 5 linhas do dataframe
exchange_rates.head()


# In[117]:


# verificando as últimas 5 linhas do dataframe
exchange_rates.tail()


# In[118]:


# extraindo as informações básicas do dataframe
exchange_rates.info()


# ### Limpeza dos Dados

# In[119]:


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

# veja o resultado nas primeiras 5 linhas
exchange_rates.head()


# In[120]:


# separa as colunas Time, Euro e Dollar para atribuir ao novo dataframe exchange_rates_to_real
exchange_rates_to_real = exchange_rates[['Time', 'Euro','US_dollar']].copy()

# analisando a coluna Euro
exchange_rates_to_real['Euro'].value_counts()


# In[121]:


# analisando a coluna US_dollar
exchange_rates_to_real['US_dollar'].value_counts()


# Note que a coluna Euro e a coluna US_dollar, em 61 e 62 linhas respectivamente  apresentam-se o caráter ‘ - ’ ao invés de valores, para não prejudicar nosso trabalho é necessário removê-las.

# In[122]:


# separados os valores que não possuem '-'.
exchange_rates_to_real = exchange_rates_to_real[exchange_rates_to_real['Euro'] != '-']
exchange_rates_to_real = exchange_rates_to_real[exchange_rates_to_real['US_dollar'] != '-']

# removendo os valores nulos
exchange_rates_to_real = exchange_rates_to_real.dropna()

# convertendo a coluna Euro e US_dollar para float
exchange_rates_to_real['Euro'] = exchange_rates_to_real['Euro'].astype(float)
exchange_rates_to_real['US_dollar'] = exchange_rates_to_real['US_dollar'].astype(float)

'''
    O conjunto de dados em questão, nos porporciona a taxa de câmbio do euro para
    diversas moedas, incluindo o real e o dolar. Para obtermos a taxa de câmbio
    do real em relação ao dolar, basta dividirmos real x euro / dolar x euro.
'''
exchange_rates_to_real['US_dollar']= exchange_rates_to_real['Euro']/exchange_rates_to_real['US_dollar']

# analisando as informações das primeiras 5 linhas de exchange_rates_to_real
exchange_rates_to_real.head()


# In[123]:


# analisando as informações das últimas 5 linhas de exchange_rates_to_real
exchange_rates_to_real.tail()


# ### Análise Gráfica

# In[16]:


# gerando um gráfico de linhas para visualizar a evolução da taxa de câmbio euro-dólar e euro_real
plt.plot(exchange_rates_to_real['Time'], exchange_rates_to_real['Euro'], c = 'g')
plt.plot(exchange_rates_to_real['Time'], exchange_rates_to_real['US_dollar'])
plt.show()


# ### Média Móvel

# #### Euro

# In[17]:


# definindo as propriedades pra figura
plt.figure(figsize=(9,6))
plt.subplot(3,2,1)
plt.plot(exchange_rates_to_real['Time'], exchange_rates_to_real['Euro'])
plt.title('Valores Originais', weight='bold')

'''
 Calculando a média móvel da coluna Euro, usando um janela móvel
 de 7 dias, de 30 dias, de 50 dias, de 100 dias e de 365 dias.
'''
for i, rolling_mean in zip([2, 3, 4, 5, 6],
                           [7, 30, 50, 100, 365]):
    plt.subplot(3,2,i)
    plt.plot(exchange_rates_to_real['Time'],
             exchange_rates_to_real['Euro'].rolling(rolling_mean).mean())
    plt.title('Janela Móvel: ' + str(rolling_mean)+' dias', weight='bold')
    
# ajusta automaticamente o preechimento entre os subplots
plt.tight_layout()
plt.show()


# #### Dólar

# In[18]:


# definindo as propriedades pra figura
plt.figure(figsize=(9,6))
plt.subplot(3,2,1)
plt.plot(exchange_rates_to_real['Time'], exchange_rates_to_real['US_dollar'])
plt.title('Valores Originais', weight='bold')

'''
 Calculando a média móvel da coluna US_dollar, usando um janela móvel
 de 7 dias, de 30 dias, de 50 dias, de 100 dias e de 365 dias.
'''
for i, rolling_mean in zip([2, 3, 4, 5, 6],
                           [7, 30, 50, 100, 365]):
    plt.subplot(3,2,i)
    plt.plot(exchange_rates_to_real['Time'],
             exchange_rates_to_real['US_dollar'].rolling(rolling_mean).mean())
    plt.title('Janela Móvel: ' + str(rolling_mean)+' dias', weight='bold')
    
# ajusta automaticamente o preechimento entre os subplots
plt.tight_layout()
plt.show()


# Perceba como o gráfico de linhas muda visualmente à medida que aumentamos a janela móvel. Isso aumenta a proporção de dados por tinta e pode ser útil se quisermos que o público se concentre apenas nas tendências de longo prazo.

# In[125]:


# definindo a janela móvel de 30 dias para utilizarmos.
exchange_rates_to_real['rolling_mean_euro'] = calc_rolling_mean(exchange_rates_to_real['Euro'],30)
exchange_rates_to_real['rolling_mean_dollar'] = calc_rolling_mean(exchange_rates_to_real['US_dollar'],30)

# análise gráfica
plt.plot(exchange_rates_to_real['Time'], exchange_rates_to_real['rolling_mean_euro'], c = 'g')
plt.plot(exchange_rates_to_real['Time'], exchange_rates_to_real['rolling_mean_dollar'])
plt.show()


# ### Análise das Taxas de Câmbio do Real em relação ao Euro durante os Governos Brasileiros entre os anos 2000 e 2021.

# In[13]:


# separando as taxas de câmbio do euro x real e dollar x real por governos.
fhc = exchange_rates_to_real.copy()[exchange_rates_to_real['Time'].dt.year < 2003]
lula = exchange_rates_to_real.copy()[(exchange_rates_to_real['Time'].dt.year >= 2003)
                             &(exchange_rates_to_real['Time'].dt.year < 2011)]
dilma = exchange_rates_to_real()[(exchange_rates_to_real['Time'].dt.year >= 2011)
                             &(exchange_rates_to_real['Time'] < '2016-08-31')]
temer = exchange_rates_to_real()[(exchange_rates_to_real['Time'] >= '2016-08-31')
                             &(exchange_rates_to_real['Time'].dt.year < 2019)]
bolsonaro = exchange_rates_to_real()[(exchange_rates_to_real['Time'].dt.year >= 2019)]


# #### Gerando o gráfico utilizando o style Fivethirtyeight

# In[90]:


# adicionando o style
import matplotlib.style as style
style.use('fivethirtyeight')

# adicionando os subplots
plt.figure(figsize=(18, 8))
ax1 = plt.subplot(2,5,1)
ax2 = plt.subplot(2,5,2)
ax3 = plt.subplot(2,5,3)
ax4 = plt.subplot(2,5,4)
ax5 = plt.subplot(2,5,5)
ax6 = plt.subplot(2,1,2)
axes = [ax1, ax2, ax3, ax4, ax5, ax6]

# fazendo alterações e adicionando as legendas aos gráficos
for ax in axes:
    ax.set_ylim(0.5, 2.0)
    ax.set_yticks([2.0, 3.0, 4.0, 5.0, 6.0, 7.0])
    ax.set_yticklabels(['2.0', '3.0','4.0','5.0', '6.0','7.0'],
                   alpha=0.3)
    ax.set_xticklabels([])
    ax.grid(alpha=0.5)     
    
# gráfico ax1: fhc
ax1.plot(fhc['Time'], fhc['rolling_mean'], color='#BF5FFF')
ax1.set_xticklabels(['', '2000', '', '', '2001','','', '2002',''], alpha=0.3)
ax1.text(730576.0, 8.0, 'FHC', fontsize=18, weight='bold', color='#BF5FFF')
ax1.text(730380.0, 7.5, '(2000-2002)', weight='bold', alpha=0.3)
    
# gráfico ax2: lula
ax2.plot(lula['Time'], lula['rolling_mean'], color='#ffa500')
ax2.set_xticklabels(['', '2002', '', '2004', '', '2006', '',
                     '2008', '', '2010'],
                   alpha=0.3)
ax2.text(732288.0, 8.0, 'LULA', fontsize=18, weight='bold', color='#ffa500')
ax2.text(731900.0, 7.5, '(2003-2010)', weight='bold', alpha=0.3)

# gráfico ax3: dilma
ax3.plot(dilma['Time'], dilma['rolling_mean'], color='#00B2EE')
ax3.set_xticklabels(['', '2011', '','        2014', '', '', '2016'], alpha=0.3)
ax3.text(734705.0, 8.0, 'DILMA', fontsize=18, weight='bold', color='#00B2EE')
ax3.text(734518.0, 7.5, '(2011-2016)', weight='bold', alpha=0.3)

# gráfico ax4: temer
ax4.plot(temer['Time'], temer['rolling_mean'], color='g')
ax4.set_xticklabels(['2016', '', '', '', '2017', '', '', '','2018'], alpha=0.3)
ax4.text(736460.0, 8.0, 'TEMER', fontsize=18, weight='bold', color='g')
ax4.text(736400.0, 7.5, '(2016-2018)', weight='bold', alpha=0.3)

# gráfico ax5: bolsonaro
ax5.plot(bolsonaro['Time'], bolsonaro['rolling_mean'], color='b')
ax5.set_xticklabels(['', '2019', '','', '2020', '','','2021', ''], alpha=0.3)
ax5.text(737185.0, 8.0, 'BOLSONARO', fontsize=18, weight='bold', color='b')
ax5.text(737230.0, 7.5, '(2019-ATUAL)', weight='bold', alpha=0.3)

# gráfico dos presidentes
ax6.plot(fhc['Time'], fhc['rolling_mean'], color='#BF5FFF')
ax6.plot(lula['Time'], lula['rolling_mean'], color='#ffa500')
ax6.plot(dilma['Time'], dilma['rolling_mean'], color='#00B2EE')
ax6.plot(temer['Time'], temer['rolling_mean'], color='g')
ax6.plot(bolsonaro['Time'], bolsonaro['rolling_mean'], color='b')
ax6.grid(alpha=0.5)
ax6.set_xticks([])

# título e subtitulo do gráfico
ax1.text(730016.0, 10.1, 'TAXA DE CÂMBIO EURO-REAL ENTRE 2000-2021',
         fontsize=20, weight='bold')
ax1.text(730016.0, 8.9, '''Taxas de câmbio EURO-REAL para os governos: 
FHC (2000 - 2002), Lula (2003 - 2010), Dilma (2011-2016), Temer (2016-2018), Bolsonaro (2019-ATUAL).''',fontsize=16)

# adicionando assinatura
ax6.text(729916.0, 0.65, 'DCA0305' + ' '*195 + 'Danilo de Sousa Lopes',
        color = '#f0f0f0', backgroundcolor = '#4d4d4d',size=14)
plt.savefig("euro_to_real.png")
plt.show()


# ### Análise das Taxas de Câmbio do Real em relação ao Dólar durante os Governos Brasileiros entre os anos 2000 e 2020.

# In[87]:


# separando as taxas de câmbio do dólar x real por governos.
fhc2 = dollar_to_real.copy()[dollar_to_real['Time'].dt.year < 2003]
lula2 = dollar_to_real.copy()[(dollar_to_real['Time'].dt.year >= 2003)
                             &(dollar_to_real['Time'].dt.year < 2011)]
dilma2 = dollar_to_real.copy()[(dollar_to_real['Time'].dt.year >= 2011)
                             &(dollar_to_real['Time'] < '2016-08-31')]
temer2 = dollar_to_real.copy()[(dollar_to_real['Time'] >= '2016-08-31')
                             &(dollar_to_real['Time'].dt.year < 2019)]
bolsonaro2 = dollar_to_real.copy()[(dollar_to_real['Time'].dt.year >= 2019)]


# In[91]:


# adicionando os subplots
plt.figure(figsize=(18, 8))
ax1 = plt.subplot(2,5,1)
ax2 = plt.subplot(2,5,2)
ax3 = plt.subplot(2,5,3)
ax4 = plt.subplot(2,5,4)
ax5 = plt.subplot(2,5,5)
ax6 = plt.subplot(2,1,2)
axes = [ax1, ax2, ax3, ax4, ax5, ax6]

# fazendo alterações e adicionando as legendas aos gráficos
for ax in axes:
    ax.set_ylim(0.5, 2.0)
    ax.set_yticks([1.0, 2.0, 3.0, 4.0, 5.0, 6.0])
    ax.set_yticklabels(['1.0', '2.0','3.0','4.0', '5.0','6.0'],
                   alpha=0.3)
    ax.set_xticklabels([])
    ax.grid(alpha=0.5)     
    
# gráfico ax1: fhc
ax1.plot(fhc2['Time'], fhc2['rolling_mean'], color='#BF5FFF')
ax1.set_xticklabels(['', '2000', '', '', '2001','','', '2002',''], alpha=0.3)
ax1.text(730576.0, 7.0, 'FHC', fontsize=18, weight='bold', color='#BF5FFF')
ax1.text(730380.0, 6.5, '(2000-2002)', weight='bold', alpha=0.3)
    
# gráfico ax2: lula
ax2.plot(lula2['Time'], lula2['rolling_mean'], color='#ffa500')
ax2.set_xticklabels(['', '2002', '', '2004', '', '2006', '',
                     '2008', '', '2010'],
                   alpha=0.3)
ax2.text(732288.0, 7.0, 'LULA', fontsize=18, weight='bold', color='#ffa500')
ax2.text(731900.0, 6.5, '(2003-2010)', weight='bold', alpha=0.3)

# gráfico ax3: dilma
ax3.plot(dilma['Time'], dilma['rolling_mean'], color='#00B2EE')
ax3.set_xticklabels(['', '2011', '','        2014', '', '', '2016'], alpha=0.3)
ax3.text(734705.0, 7.0, 'DILMA', fontsize=18, weight='bold', color='#00B2EE')
ax3.text(734518.0, 6.5, '(2011-2016)', weight='bold', alpha=0.3)

# gráfico ax4: temer
ax4.plot(temer2['Time'], temer2['rolling_mean'], color='g')
ax4.set_xticklabels(['2016', '', '', '', '2017', '', '', '','2018'], alpha=0.3)
ax4.text(736460.0, 7.0, 'TEMER', fontsize=18, weight='bold', color='g')
ax4.text(736400.0, 6.5, '(2016-2018)', weight='bold', alpha=0.3)

# gráfico ax5: bolsonaro
ax5.plot(bolsonaro2['Time'], bolsonaro2['rolling_mean'], color='b')
ax5.set_xticklabels(['', '2019', '','', '2020', '','','2021', ''], alpha=0.3)
ax5.text(737185.0, 7.0, 'BOLSONARO', fontsize=18, weight='bold', color='b')
ax5.text(737230.0, 6.5, '(2019-ATUAL)', weight='bold', alpha=0.3)

# gráfico dos presidentes
ax6.plot(fhc2['Time'], fhc2['rolling_mean'], color='#BF5FFF')
ax6.plot(lula2['Time'], lula2['rolling_mean'], color='#ffa500')
ax6.plot(dilma2['Time'], dilma2['rolling_mean'], color='#00B2EE')
ax6.plot(temer2['Time'], temer2['rolling_mean'], color='g')
ax6.plot(bolsonaro2['Time'], bolsonaro2['rolling_mean'], color='b')
ax6.grid(alpha=0.5)
ax6.set_xticks([])

# título e subtitulo do gráfico
ax1.text(730016.0, 8.9, 'TAXA DE CÂMBIO USD-REAL ENTRE 2000-2021',
         fontsize=20, weight='bold')
ax1.text(730016.0, 7.9, '''Taxas de câmbio USD-REAL para os governos: 
FHC (2000 - 2002), Lula (2003 - 2010), Dilma (2011-2016), Temer (2016-2018), Bolsonaro (2019-ATUAL).''',fontsize=16)

# adicionando assinatura
ax6.text(729916.0, 0.65, 'DCA0305' + ' '*195 + 'Danilo de Sousa Lopes',
        color = '#f0f0f0', backgroundcolor = '#4d4d4d',size=14)
plt.savefig("dollar_to_real.png")
plt.show


# ### Análise das Taxas de Câmbio do Real, contrastre entre os gráfios Euro x Real e Dólar x Real

# In[92]:


# definindo as propriedades da figura
fig, (ax1, ax2) = plt.subplots(2, sharex=True, figsize = (16,8))

# adicionando o título e subtitulo ao gráfico
ax1.text(729700.0, 8.9, 'TAXA DE CÂMBIO EURO(€) x REAL(R$) E DÓLAR(US$) x REAL(R$) ENTRE 2000-2021',
         fontsize=20, weight='bold')
ax1.text(729700.0, 7.9, '''Taxas de câmbio do REAL para os governos: FHC (2000 - 2002), Lula (2003 - 2010), Dilma (2011-2016), Temer (2016-2018), 
Bolsonaro (2019-ATUAL).''',fontsize=16)

# gráfico real x euro
ax1.plot(fhc['Time'], fhc['rolling_mean'], color='#BF5FFF', label="FHC")
ax1.plot(lula['Time'], lula['rolling_mean'], color='#ffa500', label="Lula")
ax1.plot(dilma['Time'], dilma['rolling_mean'], color='#00B2EE', label="Dilma")
ax1.plot(temer['Time'], temer['rolling_mean'], color='g', label="Temer")
ax1.plot(bolsonaro['Time'], bolsonaro['rolling_mean'], color='b', label="Bolsonaro")
ax1.set_title('EUR x BRL')
ax1.grid(alpha=0.5) 
ax1.legend()

# gráfico real x dólar
ax2.plot(fhc2['Time'], fhc2['rolling_mean'], color='#BF5FFF')
ax2.plot(lula2['Time'], lula2['rolling_mean'], color='#ffa500')
ax2.plot(dilma2['Time'], dilma2['rolling_mean'], color='#00B2EE')
ax2.plot(temer2['Time'], temer2['rolling_mean'], color='g')
ax2.plot(bolsonaro2['Time'], bolsonaro2['rolling_mean'], color='b')
ax2.set_title('USD x BRL')
ax2.grid(alpha=0.5)

# adicionando assinatura
ax2.text(729700.0, 0.33, 'DCA0305' + ' '*187 + 'Danilo de Sousa Lopes',
        color = '#f0f0f0', backgroundcolor = '#4d4d4d',size=14)
plt.savefig("euro_dollar_to_real.png")
plt.tight_layout()
plt.subplots_adjust(top=0.8, wspace=0.3)
plt.show()


# In[ ]:




