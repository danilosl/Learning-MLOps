'''
Autor: Danilo de Sousa Lopes
Data: Nov. 2021

Este presente script apresenta a solução do guided project "Exploring eBay Car Sales Data" com a aplicação dos conceitos de Clean Code. Para mais detalhes da solução verifique a versão desenvolvida no jupyter notebook. 
'''

# importando a biblioteca necessária.
import pandas as pd

# lendo o dataset autos.csv e armazenando seus dados na váriavel autos.
autos = pd.read_csv('autos.csv', encoding='Latin-1')

# vamos converter os nomes das colunas do padrão camelcase para o padrão snakecase.
map_conversion = {
    'yearOfRegistration': 'registration_year',
    'monthOfRegistration': 'registration_month',
    'notRepairedDamage': 'unrepaired_damage',
    'dateCreated': 'ad_created',
    'dateCrawled': 'date_crawled',
    'offerType': 'offer_type',
    'vehicleType': 'vehicle_type',
    'powerPS': 'power_ps',
    'fuelType': 'fuel_type',
    'nrOfPictures': 'nr_pictures',
    'postalCode': 'postal_code',
    'lastSeen': 'last_seen'
}
autos.rename(columns=map_conversion, inplace=True)

# removendo as colunas com valores iguais ou nulos.
# pylint: disable=E1101
autos = autos.drop(['nr_pictures','offer_type','seller'])

# remoção dos caracteres extras e conversão das colunas númericas armazenadas em texto.
autos['price'] = (autos['price'].str.replace('$','').str.replace(',', '').astype(float))
autos['odometer'] = (autos['odometer'].str.replace('km','').str.replace(',', '').astype(float))

# renomeando a coluna odometer para odometer_km
autos.rename(columns={"odometer": 'odometer_km'}, inplace=True)

# eliminando os outliers da coluna price
autos = autos[autos.price.between(1, 350000)]

# verificando após a remoção
autos['date_crawled'].str[:10].value_counts(normalize=True, dropna=False).sort_index()
autos['ad_created'].str[:10].value_counts(normalize=True, dropna=False).sort_index()
autos['last_seen'].str[:10].value_counts(normalize=True, dropna=False).sort_index()

# eliminando os outliers da coluna registration_year.
autos = autos[autos.registration_year.between(1910, 2016)]

# analise das 20 marcas de veículos mais populares
autos['brand'].value_counts().head(20)

# criando uma serie com as 20 marcas mais populares da lista.
top_brand = autos.brand.value_counts().head(20).index

# criando os dicionários para os preços médios e as quilometragens médias das top 20 marcas.
dict_mean_price = {}
dict_mean_odometer = {}

# interando sobre eles.
for brand in top_brand:
    mean_price = autos[autos['brand'] == brand]['price'].mean()
    mean_odometer = autos[autos['brand'] == brand]['odometer_km'].mean()
    dict_mean_price[brand] = mean_price
    dict_mean_odometer[brand] = mean_odometer

# convertendo os dicionários em séries de objetos.
series_mean_price = pd.Series(dict_mean_price)
series_mean_odometer = pd.Series(dict_mean_odometer)

# criando um dataframe com a série de objetos de preços médios.
df_relation_brand = pd.DataFrame(series_mean_price, columns=['mean_price'])
# atribuindo a série de objetos de quilometragens médias, como uma nova coluna.
df_relation_brand['mean_odometer_km'] = series_mean_odometer
df_relation_brand.sort_index()

# após a análise dos preços médios e quilometragens méidas das 20 marcas mais comuns
# não podemos perceber uma relação direta entre os dois valores.
