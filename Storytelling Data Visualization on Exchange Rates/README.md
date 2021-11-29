# MLOps - Storytelling Data Visualization on Exchange Rates

Neste projeto guiado usamos o Dataset reunido por Daria Chemkaeva e disponibilizado no Kaggle, que descreve as taxas de câmbio diárias de diversas moedas entre 1999 e 2021, com o objetivo de aplicar as principais técnicas de tratamento, limpeza de dados e visualização, para podermos gerar análises exploratórias como: as taxas de câmbio do Euro e do Dólar, em relação ao Real, entre os Governos FHC e Bolsonaro.

O objetivo deste projeto foi aplicar as principais técnicas de visualização de dados de narração de histórias e design de informação, abordados pelo curso *Storytelling Data Visualization and Information Design* na plataforma *Dataquest.io*. 

Foram implementados, ainda, conceitos de código limpo, boas práticas de programação, documentação de código com base na padronização *PEP8*, logging, testes e stylo com *FiveThirtyEight*.

Ademais, esse projeto faz parte do conjunto de projetos avaliativos referentes a disciplina PROJETO DE SISTEMAS BASEADOS EM APRENDIZADO DE MÁQUINA sob orientação do professor Ivanovitch Silva.

## Tecnologias Usadas

Para o desenvolvimento do projeto foi necessário a utilização das seguintes tecnologias open source.

- Python3
- Anaconda
- Jupyter Notebook
- Jupyter Lab
- Pylint
- Pytest
- Pandas
- Matplotlib
- Logging
- Autopep8

## Instalação

É importante destacar que o projeto foi desenvolvido através do framework Anaconda, onde uma vasta quantidade de ferramentas úteis para o estudo da Ciência de Dados, já se fazem presentes após a sua instalação e configuração. Caso seja necessário a instalação manualmente, abaixo temos os comandos necessários:

Instalação da biblioteca Autopep8 para ajudar na padronização automática do código.
```shell
$ pip install autopep8
```
Instalação da biblioteca Pylint para analisar a padronização do código.
```shell
$ pip install pylint
```
Instalação da biblioteca Pytest para realizar os testes.
```shell
$ pip install pytest pytest-sugar
```
Instalação da biblioteca Pandas para o tratamento dos dados.
```shell
$ pip install pandas
```

## Teste

Foi elaborado um conjunto de testes, com os arquivos: funcoes.py, test_funcoes.py e euro-daily_test.csv

1 - Faça uma clonagem do repositório:
```shell
$ git clone https://github.com/danilosl/Learning-MLOps.git
```
2 - Entre na pasta test:
```shell
$ cd Learning-MLOps\Storytelling Data Visualization on Exchange Rates\test
```
3 - Execute os arquivos funcoes.py
```shell
$ python3 ./funcoes.py
```
4 - Execute o arquivo de test_funcoes.py com o Pytest
```shell
$ python -m pytest test_funcoes.py
```
5 - Teste o script python utilizando o pylint.
```shell
$ pylint nome_arquivo.py
```

## Resultados

![euro_to_real](https://user-images.githubusercontent.com/77031612/143921431-1d394105-d062-4a41-83de-e0d4d64d94f6.png)

![dollar_to_real](https://user-images.githubusercontent.com/77031612/143921423-02e6c05e-e6d7-4fc9-bd34-e15a3546d7b8.png)

![euro_dollar_to_real](https://user-images.githubusercontent.com/77031612/143921430-376a1597-80ea-4ab2-94bd-f3fbb2b4768c.png)


Na primeira avaliação feita pelo pylint, o script exchange_rates.py não obteve um score aceitável, entretanto a ferramenta mostrou as devidas modificações necessárias.

![score_inicial_pylint](https://user-images.githubusercontent.com/77031612/143921433-a38f4e88-2d6b-41b1-8235-8ec78951ff23.png)

Após as modificações e  auxílios do autopep8, obteve-se o score máximo, garantindo assim uma ótima padronização com relação ao padrão PEP8.

![score_final_pylint](https://user-images.githubusercontent.com/77031612/143921432-b471fc92-506f-4874-8146-0f69a97669fd.png)
