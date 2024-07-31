import streamlit as st
import pandas as pd 
import matplotlib.pyplot as plt
import json
import requests
from apis import *


#eventos 
def enventos():
    json_url = requests.get(url)
    data = json.loads(json_url.text)

    df = pd.DataFrame(data['data'])
    print(df.head())
    df_esporte = df[[ 'discipline_name', 'name', 'status']]
    df_esporte = df_esporte.rename(columns={
        'discipline_name': 'Esporte',
        'name': 'Nome',
        'status': 'Status'

    
    })
    return df_esporte


#Ranking de Medalhas 
def ranking(num):
    
    json_url2 = requests.get(url_ranking)
    data_ranking = json.loads(json_url2.text)

    df = pd.DataFrame(data_ranking['data'])
    df_esporte = df[['rank','name', 'gold_medals', 'silver_medals', 'bronze_medals', 'total_medals']]
    df_esporte = df_esporte.rename(columns={
        'rank' : "Ranking",
        'name': 'Nome',
        'gold_medals': 'Medalha de Ouro',
        'silver_medals': 'Medalha de Prata',
        'bronze_medals': "Medalha de Bronze",
        'total_medals': "Total"
    })
    return df_esporte.head(num)
    
    
# Função para criar gráfico de medalhas por país
def grafico_medalhas(df):
    df = df.sort_values(by='Total', ascending=False).head(10)  # Mostra os top 10 países
    fig, ax = plt.subplots(figsize=(10, 6))

    ax.barh(df['Nome'], df['Medalha de Ouro'], color='gold', label='Ouro')
    ax.barh(df['Nome'], df['Medalha de Prata'], left=df['Medalha de Ouro'], color='silver', label='Prata')
    ax.barh(df['Nome'], df['Medalha de Bronze'], left=df['Medalha de Ouro'] + df['Medalha de Prata'], color='brown', label='Bronze')

    ax.set_xlabel('Número de Medalhas')
    ax.set_ylabel('Países')
    ax.set_title('Top 10 Países por Número de Medalhas')
    ax.legend()

    st.pyplot(fig)


#def update_table():
    json_url2 = requests.get(url_ranking)
    update = json.loads(json_url2.text)
    df = pd.DataFrame(update['data'])
    up = df[['name']]
    up = up.rename(columns={
        'name': 'Nome'
    })
    return up

#def jogos():
    json_url = requests.get(url_jogos)
    data = json.loads(json_url.text)
    df = pd.DataFrame(data['data'])
    df_jogos_live = df[['discipline_name']]
    return df_jogos_live


def ranking_brasil():
    '''Mostra o Ranking do Brasil na Olímpiada'''
    json_url = requests.get(url_ranking)
    json_url.raise_for_status()
    data_ranking = json.loads(json_url.text)
    if 'data' in data_ranking:
        df = pd.DataFrame(data_ranking['data'])
        df_brasil = df[df['name'] == 'Brasil']
        df_brasil = df_brasil[['rank', 'name', 'gold_medals', 'silver_medals', 'bronze_medals', 'total_medals']]
        df_brasil = df_brasil.rename(columns={
            'rank': "Ranking",
            'name': 'Nome',
            'gold_medals': 'Medalha de Ouro',
            'silver_medals': 'Medalha de Prata',
            'bronze_medals': "Medalha de Bronze",
            'total_medals': "Total"
        })
    return df_brasil.head()

st.header('Dashboard Jogos Olímpicos')
st.markdown("Página feita para te atualizar sobre os jogos Olímpicos de 2024!")

st.sidebar.image('images/image.png', width=200 )
 

st.markdown("# Ranking de Medalhas")
button_ranking = st.button('Exibir')
if button_ranking:
    st.table(ranking(15))
    grafico_medalhas(ranking(10))


st.markdown("# Eventos")
button_event = st.button(label='Exibir', key='button_event')
if button_event:
    st.table(enventos())



st.sidebar.title('GUIA')
op_sidebar = st.sidebar.selectbox('Opções de Filtro', options=('','Ranking', 'BRASIL'))
botao_side = st.sidebar.button('Buscar', key='buscar_side')

if botao_side and op_sidebar == 'Ranking':
    st.table(ranking(100))
    grafico_medalhas(ranking(100))


elif botao_side and op_sidebar == 'BRASIL':
    st.table(ranking_brasil())