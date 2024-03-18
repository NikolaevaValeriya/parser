import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px

data = pd.read_csv('coordinates.csv')


fig = px.scatter_geo(data,
                     lat='lat',
                     lon='lon',
                     hover_name='city',
                     custom_data=['country', 'insurance', 'luggage_cost', 
                                  'ticket_price', 'flight_time_minutes',
                                  'rest_rating', 'rest_price', 'hotel_rating',
                                  'lowest_hotel_price', 'highest_hotel_price'],
                     size='flight_time_minutes',  
                     color='country',     
                     projection='natural earth',
                     width=1200,
                     height=800)

fig.update_traces(hovertemplate="<b>%{hovertext}</b><br>Страна: %{customdata[0]}<br>Стоимость страховка: %{customdata[1]} ₽<br>Стоимость перевозки багажа: %{customdata[2]} ₽<br>Стоимость перелёта: %{customdata[3]:.0f} ₽<br>Время в полёте (мин.): %{customdata[4]}<br>Рейтинг ресторанов: %{customdata[5]}/5<br>Средний чек в ресторанах: %{customdata[6]} ₽<br>Рейтинг отелей: %{customdata[7]}/5<br>Средняя min стоимость отеля: %{customdata[8]} ₽<br>Средняя max стоимость отеля: %{customdata[9]} ₽<extra></extra>")

app = dash.Dash(__name__)

fig.update_layout(
    geo=dict(
        #bgcolor='powderblue', 
        landcolor='lightgreen', 
        lakecolor='lightblue',  
        showocean=True,  
        oceancolor='lightblue' 
    )
)

app.layout = html.Div([
    dcc.Graph(
        id='world-map',
        figure=fig
    )
])

if __name__ == '__main__': 
    app.run_server(debug=True)