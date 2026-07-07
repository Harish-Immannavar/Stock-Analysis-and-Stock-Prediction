import plotly.graph_objects as go
import dateutil
import datetime
import pandas_ta as pta
import streamlit as st

def plotly_table(dataframe):
    
    headerColor = '#0078ff'
    rowEvenColor = '#f8fafd'
    rowOddColor = '#e1efff'  
    
    number_of_rows = len(dataframe)
    alternating_colors = [rowOddColor if i % 2 == 0 else rowEvenColor for i in range(number_of_rows)]
    
    total_columns = 1 + len(dataframe.columns)
    column_colors = [alternating_colors for _ in range(total_columns)]

    fig = go.Figure(data=go.Table(
        header=dict(
            values=["<b>Metric</b>"] + [f"<b>{str(i)}</b>" for i in dataframe.columns],
            line_color=headerColor, 
            fill_color=headerColor, 
            align='center', 
            font=dict(color='white', size=15),
            height=35,
        ),
        cells=dict(
            values=[[f"<b>{str(i)}</b>" for i in dataframe.index]] + [dataframe[i] for i in dataframe.columns], 
            fill=dict(color=column_colors), 
            align='left',
            line_color=['white'],
            font=dict(color=["black"], size=15),
            height=30
        )
    ))
    
    fig.update_layout(height=240, margin=dict(l=0, r=0, t=0, b=0))
    return fig

def filter_data(dataframe, num_period):
    if num_period == '1mo':
        date = dataframe.index[-1] + dateutil.relativedelta.relativedelta(months=-1)
    elif num_period == '5d':
        date = dataframe.index[-1] + dateutil.relativedelta.relativedelta(days=-5)     
    elif num_period == '6mo':
        date = dataframe.index[-1] + dateutil.relativedelta.relativedelta(months=-6)
    elif num_period == '5y':
        date = dataframe.index[-1] + dateutil.relativedelta.relativedelta(years=-5)
    elif num_period == '1y':                                                    
        date = dataframe.index[-1] + dateutil.relativedelta.relativedelta(years=-1)  
    elif num_period == 'ytd':
        date = datetime.datetime(dataframe.index[-1].year, 1, 1).strftime('%Y-%m-%d')
    else:
        date = dataframe.index[0]
    
    return dataframe.reset_index()[dataframe.reset_index()['Date'] > date]

def close_chart(dataframe, num_period=False):
    if num_period:
        dataframe = filter_data(dataframe, num_period)
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=dataframe['Date'], y=dataframe['Open'], mode='lines', name='Open', line=dict(width=2, color='#5ab7ff')))
    fig.add_trace(go.Scatter(x=dataframe['Date'], y=dataframe['Close'], mode='lines', name='Close', line=dict(width=2, color='black')))
    fig.add_trace(go.Scatter(x=dataframe['Date'], y=dataframe['High'], mode='lines', name='High', line=dict(width=2, color='#0078ff')))
    fig.add_trace(go.Scatter(x=dataframe['Date'], y=dataframe['Low'], mode='lines', name='Low', line=dict(width=2, color="red")))

    # FIXED: Added showticklabels=True to both axes
    fig.update_xaxes(rangeslider_visible=True, showticklabels=True)
    fig.update_yaxes(showticklabels=True)
    fig.update_layout(height=200, margin=dict(l=0, r=20, t=20, b=0), plot_bgcolor='white', paper_bgcolor='#e1efff', legend=dict(yanchor="top", xanchor="right"))
    return fig

def candlestick(dataframe, num_period):
    dataframe = filter_data(dataframe, num_period)
    fig = go.Figure()
    fig.add_trace(go.Candlestick(x=dataframe['Date'], open=dataframe['Open'], high=dataframe['High'], low=dataframe['Low'], close=dataframe['Close']))
    fig.update_xaxes(showticklabels=True)
    fig.update_yaxes(showticklabels=True)
    fig.update_layout(showlegend=False, height=1000, margin=dict(l=0, r=0, t=0, b=0), plot_bgcolor='white', paper_bgcolor='#e1efff')
    return fig

def RSI(dataframe, num_period):
    dataframe = dataframe.copy()  
    dataframe['RSI'] = pta.rsi(dataframe['Close'])
    dataframe = filter_data(dataframe, num_period)
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=dataframe['Date'], y=dataframe.RSI, name='RSI',
                              line=dict(width=2, color='orange')))
    # Reference line at 30 (oversold threshold), fill between RSI and this line
    fig.add_trace(go.Scatter(x=dataframe['Date'], y=[30]*len(dataframe), name='Oversold (30)',
                              line=dict(width=1, color='#79da84', dash='dash'),
                              fill='tonexty'))
    # Reference line at 70 (overbought threshold)
    fig.add_trace(go.Scatter(x=dataframe['Date'], y=[70]*len(dataframe), name='Overbought (70)',
                              line=dict(width=1, color='red', dash='dash')))
    fig.update_xaxes(showticklabels=True)
    fig.update_yaxes(showticklabels=True, range=[0, 100])
    fig.update_layout(height=200, plot_bgcolor='white', paper_bgcolor="#ecc7a2",
                       margin=dict(l=0, r=0, t=0, b=0),
                       legend=dict(orientation="h", yanchor="top", y=1.02, xanchor="right", x=1))
    return fig

def Moving_average(dataframe, num_period):
    dataframe = dataframe.copy()
    dataframe['SMA_50'] = pta.sma(dataframe['Close'], 50)
    dataframe = filter_data(dataframe, num_period)
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=dataframe['Date'], y=dataframe['Open'], mode='lines', name='Open', line=dict(width=2, color='#5ab7ff')))
    fig.add_trace(go.Scatter(x=dataframe['Date'], y=dataframe['Close'], mode='lines', name='Close', line=dict(width=2, color='black')))
    fig.add_trace(go.Scatter(x=dataframe['Date'], y=dataframe['High'], mode='lines', name='High', line=dict(width=2, color='#0078ff')))
    fig.add_trace(go.Scatter(x=dataframe['Date'], y=dataframe['Low'], mode='lines', name='Low', line=dict(width=2, color="red")))
    fig.add_trace(go.Scatter(x=dataframe['Date'], y=dataframe['SMA_50'], mode='lines', name='SMA 50', line=dict(width=2, color="purple")))
    
    # FIXED: Added showticklabels=True to both axes
    fig.update_xaxes(rangeslider_visible=True, showticklabels=True)
    fig.update_yaxes(showticklabels=True)
    fig.update_layout(height=500, margin=dict(l=0, r=20, t=20, b=0), plot_bgcolor='white', paper_bgcolor='#e1efff', legend=dict(yanchor="top", xanchor="right"))
    return fig

def MACD(dataframe, num_period):
    macd = pta.macd(dataframe['Close']).iloc[:, 0]
    macd_signal = pta.macd(dataframe['Close']).iloc[:, 1]
    macd_hist = pta.macd(dataframe['Close']).iloc[:, 2]
    dataframe['MACD'] = macd
    dataframe['MACD Signal'] = macd_signal
    dataframe['MACD Hist'] = macd_hist
    dataframe = filter_data(dataframe, num_period)
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=dataframe['Date'], y=dataframe['MACD'], name='MACD', marker_color='orange', line=dict(width=2, color='orange')))
    fig.add_trace(go.Scatter(x=dataframe['Date'], y=dataframe['MACD Signal'], name='MACD Signal', marker_color='red', line=dict(width=2, color='red', dash='dash')))
    c = ['red' if cl < 0 else "green" for cl in macd_hist]
    
    # FIXED: Added showticklabels=True to both axes
    fig.update_xaxes(showticklabels=True)
    fig.update_yaxes(showticklabels=True)
    fig.update_layout(height=200, plot_bgcolor='white', paper_bgcolor='#e1efff', margin=dict(l=0, r=0, t=0, b=0), legend=dict(orientation="h", yanchor="top", y=1.02, xanchor="right", x=1))
    return fig

def Moving_average_forecast(forecast):
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=forecast.index[:-30], y=forecast['Close'].iloc[:-30],
                              mode='lines', name='Close Price', line=dict(width=2, color='black')))
    fig.add_trace(go.Scatter(x=forecast.index[-31:], y=forecast['Close'].iloc[-31:],mode='lines', name='Future Close Price',
                              line=dict(width=2, color='red')))
    # Confidence band, only if the columns exist
    if 'lower' in forecast.columns and 'upper' in forecast.columns:
        fig.add_trace(go.Scatter(x=forecast.index[-31:], y=forecast['upper'].iloc[-31:], mode='lines', line=dict(width=0), 
                                 showlegend=False))
        fig.add_trace(go.Scatter(x=forecast.index[-31:], y=forecast['lower'].iloc[-31:], mode='lines', line=dict(width=0), 
                                 fill='tonexty', fillcolor='rgba(255,0,0,0.15)', name='Confidence Interval'))
    fig.update_xaxes(rangeslider_visible=True)
    fig.update_layout(height=500, margin=dict(l=0, r=20, t=20, b=0), plot_bgcolor='white', paper_bgcolor='#e1efff', 
                      legend=dict(yanchor="top", xanchor="right"))
    return fig 