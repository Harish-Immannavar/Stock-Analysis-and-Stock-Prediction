# 📈 Stock Price Forecasting using Time Series Analysis

## Overview

This project aims to forecast future stock prices using historical market data from Yahoo Finance. The data is first preprocessed and checked for stationarity before training multiple time series forecasting models. A Streamlit-based web application allows users to visualize historical trends, compare model performance, and generate future price predictions.


## Features

- Fetches historical stock data using Yahoo Finance
- Performs data preprocessing and stationarity testing (ADF Test)
- Implements Moving Average, ARIMA, SARIMA, and Prophet models
- Compares models using RMSE
- Generates a 30-day stock price forecast
- Interactive visualizations using Plotly and Streamlit



## Tech Stack

**Python, Pandas, NumPy, yfinance, Statsmodels, Prophet, Plotly, Streamlit, Scikit-learn**



## Project Workflow

1. Retrieve historical stock price data.
2. Preprocess the data and perform stationarity analysis.
3. Train multiple forecasting models.
4. Evaluate each model using RMSE.
5. Select the best-performing model.
6. Forecast future stock prices and visualize the results.

---

## Conclusion

This project demonstrates how different time series forecasting models can be used to predict stock prices and how their performance varies for the same dataset. By comparing multiple approaches and selecting the model with the lowest RMSE, the application provides a simple and effective framework for stock price forecasting while giving users an interactive way to explore historical trends and future predictions.
