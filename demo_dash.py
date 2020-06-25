import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.dates as mdates
import plotly.express as px
import plotly.graph_objects as go
import dash
import dash_core_components as dcc
import dash_html_components as html


#-----------------------------------------------------------------------------#
casos_estado = pd.read_csv('data/casos_mortes_por_estado.csv')
casos_brasil = pd.read_csv('data/casos_brasil_por_data.csv')

states = casos_estado['state'].unique()

fig1 = go.Figure()
fig1.add_trace(go.Scatter(x=casos_brasil['date'], y=casos_brasil['new_confirmed'].cumsum(),name='Brasil'))

for state in states:
    cond = casos_estado['state'] == state
    sub = casos_estado[cond]
    
    fig1.add_trace(go.Scatter(x=sub['date'], y=sub['new_confirmed'].cumsum(),name=state))

fig1.update_layout(height=600, width=900,title_text='Casos acumulados de COVID-19 no Brasil',xaxis_title="Datas",
    yaxis_title="Número de Casos",xaxis_rangeslider_visible=True)
#-----------------------------------------------------------------------------#

states = casos_estado['state'].unique()

fig2 = go.Figure()

fig2.add_trace(go.Scatter(x=casos_brasil['date'], y=casos_brasil['new_deaths'].cumsum(),name='Brasil'))
for state in states:
    cond = casos_estado['state'] == state
    sub = casos_estado[cond]
    
    fig2.add_trace(go.Scatter(x=sub['date'], y=sub['new_deaths'].cumsum(),name=state))

fig2.update_layout(height=600, width=900,title_text='Mortes acumuladas de COVID-19 no Brasil',xaxis_title="Datas",
    yaxis_title="Número de Mortes",xaxis_rangeslider_visible=True)
#-----------------------------------------------------------------------------#
taxa_mortes = pd.read_csv('data/taxa_de_mortes.csv')
data = pd.read_csv('data/pre_processed_data.csv')
states = taxa_mortes['state'].unique()

fig3 = go.Figure()
fig3.add_trace(go.Bar(x=['Brasil'], y=[data['new_deaths'].sum()/data['new_confirmed'].sum()],name='Brasil'))
for state in states:
    cond = taxa_mortes['state'] == state
    sub = taxa_mortes[cond]
    
    fig3.add_trace(go.Bar(x=sub['state'], y=sub['taxa_de_mortes']*100,name=state))

fig3.update_layout(height=600, width=900,title_text='Taxas de mortes de COVID-19 no Brasil por estados',
    yaxis_title="Taxas de mortes (%)",xaxis_rangeslider_visible=True,xaxis={'categoryorder':'total descending'})
#-----------------------------------------------------------------------------#

states = casos_estado['state'].unique()

fig4 = go.Figure()
fig4.add_trace(go.Scatter(x=casos_brasil['date'], y=casos_brasil['new_deaths'].cumsum()/casos_brasil['new_confirmed'].cumsum(),name='Brasil'))

for state in states:
    cond = casos_estado['state'] == state
    sub = casos_estado[cond]
    
    death_rate = sub['new_deaths'].cumsum()/sub['new_confirmed'].cumsum()
    
    fig4.add_trace(go.Scatter(x=sub['date'], y=death_rate*100,name=state))

fig4.update_layout(height=600, width=900,title_text='Taxas de mortes de COVID-19 no Brasil através do tempo',xaxis_title="Datas",
    yaxis_title="Taxa de Mortes (%)",xaxis_rangeslider_visible=True)

#-----------------------------------------------------------------------------#
taxa_infec = pd.read_csv('data/taxa_de_infec.csv')
pop_total=taxa_infec['estimated_population_2019'].sum()
casos_brasil['taxa_de_infecção'] = casos_brasil['new_confirmed'].cumsum()/pop_total

states = taxa_infec['state'].unique()

fig5 = go.Figure()
fig5.add_trace(go.Bar(x=['Brasil'], y=[casos_brasil['new_confirmed'].sum()/pop_total],name='Brasil'))
for state in states:
    cond = taxa_infec['state'] == state
    sub = taxa_infec[cond]
    
    fig5.add_trace(go.Bar(x=sub['state'], y=sub['taxa_da_população_infectada']*100,name=state))

fig5.update_layout(height=600, width=900,title_text='Taxas de população infectada por COVID-19 no Brasil por estados',
    yaxis_title="Taxa de infecção (%)",xaxis_rangeslider_visible=True,xaxis={'categoryorder':'total descending'})
#-----------------------------------------------------------------------------#

states = taxa_infec['state'].unique()

fig6 = go.Figure()
fig6.add_trace(go.Scatter(x=casos_brasil['date'], y=casos_brasil['taxa_de_infecção'],name='Brasil'))

for state in states:
    cond = casos_estado['state'] == state
    sub = casos_estado[cond]
    
    cond2 = taxa_infec['state'] == state
    sub2 = taxa_infec[cond2]
    
    infec_rate = sub['new_confirmed'].cumsum() / sub2['estimated_population_2019'].values
    fig6.add_trace(go.Scatter(x=sub['date'], y=infec_rate*100,name=state))

fig6.update_layout(height=600, width=900,title_text='Taxa de população do Brasil infectada por COVID-19 através do tempo',xaxis_title="Datas",
    yaxis_title="Taxa de Infecção(%)",xaxis_rangeslider_visible=True)



external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

colors = {
    'text': 'teal'
}

app.layout = html.Div(children=[
    html.H1(
        children='Indicadores COVID-19 no Brasil',
        style={
            'textAlign': 'center',
            'color': colors['text'],
            'border': '2em',
        }
    ),

    html.Div(children='Case estagiário de Data Science - FortBrasil', style={
        'textAlign': 'center',
        'color': colors['text']
    }),

    html.Div(style={'width':'50%',
                    'float':'left'},
             children=[
        html.H3(
            children='1 - Casos Acumulados',
            style={
            'textAlign': 'left',
            'color': colors['text']
        }
            ),
        dcc.Graph(
        id='example-graph-1',
        figure=fig1)
    ]),
    
    html.Div(style={'width':'50%',
                    'float':'right'},
             children=[
        html.H3(
            children='2 - Mortes Acumuladas',
            style={
            'textAlign': 'left',
            'color': colors['text']
        }
            ),
        dcc.Graph(
        id='example-graph-2',
        figure=fig2)
    ]),
    
    html.H3(
            children='3 - Taxa de Mortes',
            style={
            'textAlign': 'center',
            'color': colors['text']
        }
            ),
    html.Div(style={'width':'50%',
                    'float':'left'},
             children=[
        dcc.Graph(
        id='example-graph-3',
        figure=fig3)
    ]),
    html.Div(style={'width':'50%',
                    'float':'right'},
             children=[
        dcc.Graph(
        id='example-graph-4',
        figure=fig4)
    ]),
    
    html.H3(
            children='4 - Taxa de Infecção',
            style={
            'textAlign': 'center',
            'color': colors['text']
        }
            ),
    html.Div(style={'width':'50%',
                    'float':'left'},
             children=[
        dcc.Graph(
        id='example-graph-5',
        figure=fig5)
    ]),
    html.Div(style={'width':'50%',
                    'float':'right'},
             children=[
        dcc.Graph(
        id='example-graph-6',
        figure=fig6)
    ])
])

if __name__ == '__main__':
    app.run_server(debug=True)