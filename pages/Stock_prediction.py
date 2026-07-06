import streamlit as st
from pages.utils.model_train import get_data, get_differencing_order,scaling,evaluate_model,get_rolling_mean,get_forecast,inverse_scaling
import pandas as pd
from pages.utils.plotly_figures import plotly_table,Moving_average_forecast

st.set_page_config(
    page_title="Stock Prediction",
    page_icon="📉",
    layout="wide",
)

st.title("Stock Prediction")
col1,col2,col3 = st.columns(3)
with col1:
    ticker = st.text_input('Stock ticker','AAPL')

rmse = 0

st.subheader('Predicting next 30 days close Price for:'+ticker)

close_price = get_data(ticker)
rolling_price = get_rolling_mean(close_price)

differencing_order = get_differencing_order(rolling_price)
scaled_data,scaler = scaling(rolling_price)
scaled_data = scaled_data.flatten()
rmse = evaluate_model(scaled_data,differencing_order)

st.write("**Model Rmse Score**",rmse)
forecast = get_forecast(scaled_data,differencing_order)
forecast['Close'] = inverse_scaling(
    scaler,
    forecast['Close']
).flatten()
st.write('##### Forecast Data(Next 30 Days)')
fig_tail = plotly_table (forecast.sort_index(ascending=True).round(3))
fig_tail.update_layout(height=220)
st.plotly_chart(fig_tail,use_container_width=True)


# Flatten column MultiIndex if present
if isinstance(rolling_price.columns, pd.MultiIndex):
    rolling_price.columns = rolling_price.columns.get_level_values(0)

if isinstance(forecast.columns, pd.MultiIndex):
    forecast.columns = forecast.columns.get_level_values(0)



combined = pd.concat([rolling_price, forecast])


st.plotly_chart(
    Moving_average_forecast(combined.iloc[250:]),
    use_container_width=True
)
