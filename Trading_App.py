import streamlit as st

st.set_page_config(
    page_title = "Trading App",
    page_icon = ":heavy_dollar_sign:",
    layout =   "wide"
)

st.title("Trading Guide App:bar_chart:")

st.header("We provide the greatest platforms for you to collect all information prior to investing in stocks.")

st.image("app.png")

st.markdown("## We provide the follwing services:")

st.markdown("#### :one: Stock Information")
st.write("Through this page, you can see all information about stock. ")

st.markdown("#### :two: Stock Prediction")
st.write(" You can explore predicted closing prices for the next 30 days based on historical stock data and advanced forecasting mdoels. Use this tool to gain valuable insights into market trends and make informed investment decisions. ")

st.markdown("#### :three: CAPM Return")
st.write(" Discover how the Capital Price Modelling(CAP) calculates the expected return of different stocks asset based on its risk and market performance.")

st.markdown("#### :four: CAPM Beta")