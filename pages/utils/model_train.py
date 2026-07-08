import yfinance as yf
from statsmodels.tsa.stattools import adfuller
from sklearn.metrics import mean_squared_error,r2_score
from statsmodels.tsa.arima.model import ARIMA
from prophet import Prophet
from statsmodels.tsa.statespace.sarimax import SARIMAX
import numpy as np
from sklearn.preprocessing import StandardScaler
from datetime import    datetime,timedelta
import pandas as pd

def get_data(ticker):
    stock_data =   yf.download(ticker,start='2024-01-01')
    return stock_data[['Close']]

def Stationary_check(close_price):
    adf_test = adfuller(close_price.squeeze())
    p_value = round(adf_test[1],3)
    return p_value

def get_rolling_mean (close_price):
    rolling_price = close_price.rolling(window=7).mean().dropna()
    return rolling_price

def get_differencing_order(close_price):

    p_value =   Stationary_check(close_price)
    d=0
    while True:
        if p_value>0.05:
            d+=1
            close_price= close_price.diff().dropna()
            p_value = Stationary_check(close_price)
        else:
            break
    return d

def get_best_order(data, d):
    best_aic = float("inf")
    best_order = (1, d, 1)

    for p in range(6):
        for q in range(6):
            try:
                model = ARIMA(data, order=(p, d, q))
                result = model.fit()

                if result.aic < best_aic:
                    best_aic = result.aic
                    best_order = (p, d, q)

            except:
                continue

    return best_order

def arima_model(train, test, order):
    # Convert training data to a list so we can dynamically append to it
    history = list(train.values)
    predictions = []
    
    # Loop through every single day in our test set
    for actual_price in test.values:
        # Fit the model on our updated history
        model = ARIMA(history, order=order)
        model_fit = model.fit()
        
        # Forecast exactly 1 step ahead
        output = model_fit.forecast(steps=1)
        yhat = output[0]
        predictions.append(yhat)
        
        # CRITICAL: Add the actual observed price back into our history for the next day
        #history.append(actual_price)
        
    # Calculate RMSE based on our day-by-day rolling predictions
    rmse = np.sqrt(mean_squared_error(test, predictions))
    return rmse

def sarima_model(train, test, order):

    model = SARIMAX(
        train,
        order=order,
        seasonal_order=(1,1,1,12)
    )

    model_fit = model.fit(disp=False)

    prediction = model_fit.forecast(len(test))

    rmse = np.sqrt(mean_squared_error(test, prediction))

    return rmse


def prophet_model(train, test):

    train_df = pd.DataFrame({
        "ds": train.index,
        "y": train.values
    })

    model = Prophet(
        daily_seasonality=True
    )

    model.fit(train_df)

    future = model.make_future_dataframe(
        periods=len(test),
        freq="B"
    )

    forecast = model.predict(future)

    prediction = forecast["yhat"].tail(len(test)).values

    rmse = np.sqrt(
        mean_squared_error(test.values, prediction)
    )

    return rmse

def naive_baseline_model(train, test):
    """
    Predicts that every day in the test set will just be 
    the very last closing price observed in the training set.
    """
    # Grab the last known price from the training data
    last_known_price = train.iloc[-1]
    
    # Create an array of predictions that is just this price repeated
    predictions = np.full(shape=len(test), fill_value=last_known_price)
    
    # Calculate RMSE
    rmse = np.sqrt(mean_squared_error(test, predictions))
    
    return rmse


def compare_models(close_price):

    train = close_price[:-30]

    test = close_price[-30:]

    d = get_differencing_order(train)

    order = get_best_order(train, d)

    results = {}

    

    results["ARIMA"] = arima_model(
        train,
        test,
        order
    )

    results["SARIMA"] = sarima_model(
        train,
        test,
        order
    )

    results["Prophet"] = prophet_model(
        train,
        test
    )

    results["Naive Baseline"] = naive_baseline_model(train, test)

    best_model = min(
        results,
        key=results.get
    )

    return results, best_model


#def evaluate_model(original_price,differencing_order):
    train_data,test_data = original_price[:-30],original_price[-30:]
    predictions= fit_model(train_data, differencing_order)
    rmse =  np.sqrt(mean_squared_error  (test_data,predictions))
    return round(rmse,2)

def scaling(close_price):
    scaler =StandardScaler()
    scaled_data = scaler.fit_transform( np.array(close_price).reshape(-1,1))
    return scaled_data,scaler

def get_forecast(original_price):

    results, best_model = compare_models(original_price)

    last_date = original_price.index[-1]

    forecast_index = pd.date_range(
        start=last_date + pd.offsets.BDay(1),
        periods=30,
        freq="B"
    )

    if best_model == "ARIMA":

        d = get_differencing_order(original_price)

        order = get_best_order(
            original_price,
            d
        )

        model = ARIMA(
            original_price,
            order=order
        )

        model_fit = model.fit()

        prediction = model_fit.forecast(
            steps=30
        )


    elif best_model == "SARIMA":

        d = get_differencing_order(original_price)

        order = get_best_order(
            original_price,
            d
        )

        model = SARIMAX(
            original_price,
            order=order,
            seasonal_order=(1,1,1,12)
        )

        model_fit = model.fit(disp=False)

        prediction = model_fit.forecast(
            steps=30
        )


    elif best_model == "Prophet":

        train_df = pd.DataFrame({
            "ds": original_price.index,
            "y": original_price.values
        })

        model = Prophet(
            daily_seasonality=True
        )

        model.fit(train_df)


        future = model.make_future_dataframe(
            periods=30,
            freq="B"
        )

        forecast = model.predict(future)

        prediction = forecast["yhat"].tail(30).values



    forecast_df = pd.DataFrame(
        {
            "Close": prediction.values
        },
        index=forecast_index
    )


    return forecast_df

    

def inverse_scaling(scaler,scaled_data):
    close_price= scaler.inverse_transform(np.array(scaled_data).reshape(-1,1))
    return close_price  