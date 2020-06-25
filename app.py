import numpy as np
import pandas as pd
import plotly.graph_objects as go
import dash
import dash_core_components as dcc
import dash_html_components as html
import os

casos_estado = pd.read_csv('data/casos_mortes_por_estado.csv')
casos_brasil = pd.read_csv('data/casos_brasil_por_data.csv')
taxa_mortes = pd.read_csv('data/taxa_de_mortes.csv')
data = pd.read_csv('data/pre_processed_data.csv')
taxa_infec = pd.read_csv('data/taxa_de_infec.csv')
pop_total=taxa_infec['estimated_population_2019'].sum()
casos_brasil['taxa_de_infecção'] = casos_brasil['new_confirmed'].cumsum()/pop_total

states = casos_estado['state'].unique()

def plot_line(column,title,xlabel,ylabel):
    fig = go.Figure()
    
    if column == 'death_rate': 
        fig.add_trace(go.Scatter(x=casos_brasil['date'], y=casos_brasil['new_deaths'].cumsum()/casos_brasil['new_confirmed'].cumsum(),name='Brasil'))

    elif column == 'infec_rate': 
        fig.add_trace(go.Scatter(x=casos_brasil['date'], y=casos_brasil['taxa_de_infecção'],name='Brasil'))
        
    else:
        fig.add_trace(go.Scatter(x=casos_brasil['date'], y=casos_brasil[column].cumsum(),name='Brasil'))

    for state in states:
        cond = casos_estado['state'] == state
        sub = casos_estado[cond]

        if column == 'death_rate':
            death_rate = sub['new_deaths'].cumsum()/sub['new_confirmed'].cumsum()
            fig.add_trace(go.Scatter(x=sub['date'], y=death_rate*100,name=state))
            
        elif column == 'infec_rate':
            cond2 = taxa_infec['state'] == state
            sub2 = taxa_infec[cond2]

            infec_rate = sub['new_confirmed'].cumsum() / sub2['estimated_population_2019'].values
            fig.add_trace(go.Scatter(x=sub['date'], y=infec_rate*100,name=state))
            
        else:
            fig.add_trace(go.Scatter(x=sub['date'], y=sub[column].cumsum(),name=state))

    fig.update_layout(height=600, width=900,
                      title_text=title,
                      xaxis_title=xlabel,
                      yaxis_title=ylabel,
                      xaxis_rangeslider_visible=True)

    return fig

def plot_bar(column,title,ylabel):
    fig = go.Figure()
    
    if column == 'death_rate':
        fig.add_trace(go.Bar(x=['Brasil'], y=[data['new_deaths'].sum()/data['new_confirmed'].sum()],name='Brasil'))
    elif column == 'infec_rate':
        fig.add_trace(go.Bar(x=['Brasil'], y=[casos_brasil['new_confirmed'].sum()/pop_total],name='Brasil'))

    
    for state in states:
        if column == 'death_rate':
            cond = taxa_mortes['state'] == state
            sub = taxa_mortes[cond]
            
            fig.add_trace(go.Bar(x=sub['state'], y=sub['taxa_de_mortes']*100,name=state))
        elif column == 'infec_rate':
            cond = taxa_infec['state'] == state
            sub = taxa_infec[cond]
            
            fig.add_trace(go.Bar(x=sub['state'], y=sub['taxa_da_população_infectada']*100,name=state))
    
    
    fig.update_layout(height=600, width=900,
                      title_text=title,
                      yaxis_title=ylabel,
                      xaxis_rangeslider_visible=True,
                      xaxis={'categoryorder':'total descending'})
    
    return fig


fig1 = plot_line('new_confirmed',
                 title='Casos acumulados de COVID-19 no Brasil',
                 xlabel='Datas',
                 ylabel='Número de Casos')

fig2 = plot_line('new_deaths',
                 title='Mortes acumuladas de COVID-19 no Brasil',
                 xlabel='Datas',
                 ylabel='Número de Mortes')

fig3 = plot_bar('death_rate',
                 title='Taxas de mortes de COVID-19 no Brasil por estados',
                 ylabel='Taxas de mortes (%)')

fig4 = plot_line('death_rate',
                 title='Taxas de mortes de COVID-19 no Brasil através do tempo',
                 xlabel='Datas',
                 ylabel='Taxa de Mortes (%)')

fig5 = plot_bar('infec_rate',
                 title='Taxas de população infectada por COVID-19 no Brasil por estados',
                 ylabel='Taxa de infecção (%)')

fig6 = plot_line('infec_rate',
                 title='Taxa de população do Brasil infectada por COVID-19 através do tempo',
                 xlabel='Datas',
                 ylabel='Taxa de Infecção(%)')


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server
app.title='COVID-19'

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

    html.Div(children='Case estagiário de Data Science - FortBrasil - Claudemir Woche', style={
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
    app.run_server(debug=True, port=int(os.environ.get("PORT", 5000)), host='0.0.0.0')