import plotly
import plotly.graph_objs as go
import plotly.offline as offline
import pandas as pd

plotly.tools.set_credentials_file(username='doal7262', api_key='d2LaHa4QeroxkATku0uI')

df = pd.read_csv('weather.csv', parse_dates={'Date' : [0,1,2]})

Tmax = go.Scatter(
    name='Temp Max',
    x=df['Date'],
    y=df['tmax'],
    mode='lines',
    marker=dict(color="darkgrey"),
    line=dict(width=0),
    fillcolor='rgba(68, 68, 68, 0.3)',
    fill='tonexty' )

Tavg = go.Scatter(
    name='Temp Avg',
    x=df['Date'],
    y=(df['tmax']+df['tmin'])/2,
    mode='lines',
    line=dict(color='rgb(31, 119, 180)'),
    fillcolor='rgba(68, 68, 68, 0.3)',
    fill='tonexty' )

Tmin = go.Scatter(
    name='Temp Min',
    x=df['Date'],
    y=df['tmin'],
    marker=dict(color="darkgrey"),
    line=dict(width=0),
    mode='lines' )

Precip = go.Bar(
    name='Precipitation',
    x=df['Date'],
    y=df['precip'],
    visible=False)

Snow = go.Bar(
    name='Snow',
    x=df['Date'],
    y=df['snow'],
    visible=False
)

SnowCover = go.Bar(
    name='SnowCover',
    x=df['Date'],
    y=df['snowcover'],
    marker=dict(color="darkgrey"),
    visible=False
)

data = [Tmin, Tavg, Tmax, Precip, Snow, SnowCover]

updatemenus = list([
    dict(active=0,
         buttons=list([
            dict(label = 'Temperature',
                 method = 'update',
                 args = [{'visible': [True, True, True, False, False, False]},
                         {'title': 'Temperature in Boulder, Colorado',
                          'yaxis': {'title': 'Temperature (F)'},
                          'annotations': Tavg}]),  
            dict(label = 'Precip',
                 method = 'update',
                 args = [{'visible': [False, False, False, True, False, False]},
                         {'title': 'Precipiation in Boulder, Colorado',
                          'yaxis': {'title': 'Precipiation'},
                          'annotations': Precip}]),
            dict(label = 'Snow',
                 method = 'update',
                 args = [{'visible': [False, False, False, False, True, True]},
                         {'title': 'Snowfall in Boulder, Colorado',
                          'yaxis': {'title': 'Snow (inches)'},
                          'annotations': Precip}])
        ]),
    )
])


layout = dict(
    title='Weather in Boulder, Colorado',
    yaxis = dict(
        title= 'Temperature (F)'
    ),
    xaxis=dict(
        rangeselector=dict(
            buttons=list([
                dict(count=1,
                     label='1m',
                     step='month',
                     stepmode='backward'),
                dict(count=6,
                     label='6m',
                     step='month',
                     stepmode='backward'),
                dict(count=1,
                    label='YTD',
                    step='year',
                    stepmode='todate'),
                dict(count=1,
                    label='1y',
                    step='year',
                    stepmode='backward'),
                dict(count=10,
                    label='10y',
                    step='year',
                    stepmode='backward'),
                dict(step='all'),
            ])
        ),
        rangeslider=dict(
            visible = True
        ),
        type='date',
        scaleratio=.1,
        constrain='domain',
    ),
    updatemenus=updatemenus
    
)

fig = dict(data=data, layout=layout)

initial_range = [
    '2017-07-30', '2018-07-30'
]

fig['layout']['xaxis'].update(range=initial_range)

offline.plot(fig, filename='WeatherGraph.html')