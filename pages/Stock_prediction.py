import streamlit as st
from pages.utils.model_train import get_data, get_differencing_order,scaling,get_rolling_mean,get_forecast,inverse_scaling, compare_models
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



st.subheader('Predicting next 30 days close Price for:'+ticker)

close_price = get_data(ticker).squeeze()
#rolling_price = get_rolling_mean(close_price.squeeze())
print(close_price.head())

differencing_order = get_differencing_order(close_price)
#scaled_data,scaler = scaling(rolling_price)
#scaled_data = scaled_data.flatten()
results, best_model = compare_models(
    close_price
)
st.subheader("Model Comparison")

results_df = pd.DataFrame(
    results.items(),
    columns=["Model","RMSE"]
)

st.dataframe(results_df)

st.success(
    f"Best Model : {best_model}"
)


forecast = get_forecast(close_price)
#forecast['Close'] = inverse_scaling(scaler,forecast['Close']).flatten()
st.write('##### Forecast Data(Next 30 Days)')
fig_tail = plotly_table (forecast.sort_index(ascending=True).round(3))
fig_tail.update_layout(height=220)
st.plotly_chart(fig_tail,use_container_width=True)






combined = pd.concat([
    close_price.to_frame(name="Close"),
    forecast
])


st.plotly_chart(
    Moving_average_forecast(combined.iloc[100:]),
    use_container_width=True
)
