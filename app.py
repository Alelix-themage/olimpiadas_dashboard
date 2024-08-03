import streamlit as st
import pandas as pd 
import matplotlib.pyplot as plt
import json
import requests
from apis import *

url_esportes = 'https://apis.codante.io/olympic-games/disciplines'

#eventos 
def eventos():
    json_url = requests.get(url)
    data = json.loads(json_url.text)

    df = pd.DataFrame(data['data'])
    df_esporte = df[['discipline_name', 'name', 'status']]
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
    #Para a visualização das bandeiras
    df['Bandeira'] = df['flag_url'].apply(lambda x: f'<img src="{x}" width="50" height="30">')
    df_esporte = df[['rank', 'Bandeira', 'name', 'gold_medals', 'silver_medals', 'bronze_medals', 'total_medals']]
    df_esporte = df_esporte.rename(columns={
        'rank': "Ranking",
        'Bandeira': 'Bandeira',
        'name': 'Nome',
        'gold_medals': 'Ouro',
        'silver_medals': 'Prata',
        'bronze_medals': "Bronze",
        'total_medals': "Total"
    })
    return df_esporte.head(num)

# Função para criar gráfico de medalhas por país
def grafico_medalhas(df):
    df = df.sort_values(by='Total', ascending=False).head(10)  # Mostra os top 10 países
    fig, ax = plt.subplots(figsize=(10, 6))

    ax.barh(df['Nome'], df['Ouro'], color='gold', label='Ouro')
    ax.barh(df['Nome'], df['Prata'], left=df['Ouro'], color='silver', label='Prata')
    ax.barh(df['Nome'], df['Bronze'], left=df['Ouro'] + df['Prata'], color='brown', label='Bronze')

    ax.set_xlabel('Número de Medalhas')
    ax.set_ylabel('Países')
    ax.set_title('Top 10 Países por Número de Medalhas')
    ax.legend()

    st.pyplot(fig)

# Função para mostrar o ranking do Brasil
def ranking_brasil():
    json_url = requests.get(url_ranking)
    json_url.raise_for_status()
    data_ranking = json.loads(json_url.text)
    if 'data' in data_ranking:
        df = pd.DataFrame(data_ranking['data']) 
        df['Bandeira'] = df['flag_url'].apply(lambda x: f'<img src="{x}" width="50" height="30">')
        df_brasil = df[df['name'] == 'Brasil']
        df_brasil = df_brasil[['rank',  'Bandeira', 'name', 'gold_medals', 'silver_medals', 'bronze_medals', 'total_medals']]
        df_brasil = df_brasil.rename(columns={
            'rank': "Ranking",
            'flag_url': 'Bandeira',
            'name': 'Nome',
            'gold_medals': 'Ouro',
            'silver_medals': 'Prata',
            'bronze_medals': "Bronze",
            'total_medals': "Total"
        })
    return df_brasil

def esportes():
    json_urls = requests.get(url_esportes)
    data = json.loads(json_urls.text)
    df = pd.DataFrame(data['data'])
    df['Emblema'] = df['pictogram_url'].apply(lambda x: f'<img src="{x}" height="100px" style="background: white;">')
    data_esporte = df[['id', 'name', 'Emblema']]
    data_esporte = data_esporte.rename( columns={
        'id': 'Abreviação',
        'name': 'Nome',
        'pictogram_url': 'Emblema'
    })
    return data_esporte

#Titulo na aba do site
st.set_page_config(
    page_title="Dashboard Olímpico",  
    page_icon="🏅",  
    layout="centered",  
    initial_sidebar_state="auto",  
)
    
st.header('Dashboard Jogos Olímpicos')
st.markdown("Página feita para te atualizar sobre os jogos Olímpicos de 2024!")

st.sidebar.image('images/image.png', width=200)

st.markdown("## Posição do Brasil:")
df_brazil = ranking_brasil()
st.markdown(df_brazil.to_html(escape=False, index=False), unsafe_allow_html=True)

st.markdown("# Ranking de Medalhas")
button_ranking = st.button('Exibir')
if button_ranking:
    df_ranking = ranking(15)
    st.markdown(df_ranking.to_html(escape=False, index=False), unsafe_allow_html=True)
    grafico_medalhas(df_ranking)

st.markdown("# Eventos")
button_event = st.button(label='Exibir', key='button_event')
if button_event:
    st.table(eventos())

st.sidebar.title('GUIA')
op_sidebar = st.sidebar.selectbox('Opções de Filtro', options=('','Ranking', 'Esportes'))


if op_sidebar == 'Ranking':
    df_ranking = ranking(100)
    st.markdown(df_ranking.to_html(escape=False, index=False), unsafe_allow_html=True)
    grafico_medalhas(df_ranking)

elif op_sidebar == 'Esportes':
    df_esporte = esportes()
    st.markdown(df_esporte.to_html(escape=False, index=False), unsafe_allow_html=True)
    

st.markdown(
    """
    <style>
    .footer {
        position: ;
        bottom: 0;
        width: 100%;
        text-align: center;
        padding: 10px;
        font-size: 12px;
    }
    </style>
    <div class="footer">
        <p>© 2024 Alessandro Junior - Todos os direitos reservados.</p>
        <p><a href="https://github.com/Alelix-themage/olimpiadas_dashboard" target="_blank">Repositório no GitHub</a></p>
    </div>
    """,
    unsafe_allow_html=True
)
