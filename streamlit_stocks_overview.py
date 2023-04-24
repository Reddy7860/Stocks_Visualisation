import streamlit as st
import yfinance as yf
import plotly.graph_objs as go
import pandas as pd
from pmdarima.arima import auto_arima
from arch import arch_model
import numpy as np
import datetime


# Set page configuration
page_layout = {
    "page_title": "Stock Analysis App",
    "page_icon": ":chart_with_upwards_trend:",
    "layout": "wide",
    "initial_sidebar_state": "expanded",
}

st.set_page_config(**page_layout)

st.cache_data()
def unix_time_to_datetime(unix_time):
    return datetime.datetime.fromtimestamp(unix_time)

st.cache_data()
# Create function to fetch company info
def get_company_info(ticker):
    # Fetch ticker data from Yahoo Finance API
    ticker_info = yf.Ticker(ticker)
    
    # Get company info
    info = ticker_info.info

    print(info)

    # Get long business summary
    long_business_summary = info['longBusinessSummary']
    
    # Create dataframe with relevant company info
    df = pd.DataFrame({
        'Previous Close': info['regularMarketPreviousClose'],
        'Open': info['regularMarketOpen'],
        'Day\'s Range': f"{info['regularMarketDayLow']:.2f} - {info['regularMarketDayHigh']:.2f}",
        '52 Week Range': f"{info['fiftyTwoWeekLow']:.2f} - {info['fiftyTwoWeekHigh']:.2f}",
        'Volume': info['regularMarketVolume'],
        'Avg. Volume': info['averageVolume10days'],
        'Market Cap': info['marketCap'],
        'EPS (TTM)': info['trailingEps'],
        'Sector': info['sector'],
        'Industry': info['industry'],
        'Beta': info['beta'],
        'Payout Ratio': info['payoutRatio'],
        'Forward P/E': info['forwardPE'],
        'Price/Sales (TTM)': info['priceToSalesTrailing12Months'],
        'Price/Book (MRQ)': info['priceToBook'],
        'Profit Margin': info['profitMargins'],
        'Operating Margin (TTM)': info['operatingMargins'],
        'Return on Assets (TTM)': info['returnOnAssets'],
        'Return on Equity (TTM)': info['returnOnEquity'],
        'Revenue (TTM)': info['totalRevenue'],
        'Gross Profit (TTM)': info['grossProfits'],
        'EBITDA (TTM)': info['ebitda'],
        'Net Income (TTM)': info['netIncomeToCommon'],
        'Total Cash (MRQ)': info['totalCash'],
        'Total Debt (MRQ)': info['totalDebt'],
        'Current Ratio (MRQ)': info['currentRatio'],
        'Quick Ratio (MRQ)': info['quickRatio'],
        'Short Ratio (MRQ)': info['shortRatio']
    }, index=[0])
    
    # Set index name to ticker symbol
    df.index.name = 'Symbol'

    df = df.transpose()

    # Create text for long business summary
    summary_text = f"{ticker}: {long_business_summary}"
    
    return df, summary_text

st.cache_data()
# Create function to fetch stock price data for the last 5 years
def get_stock_price_data(ticker):
    # Fetch ticker data from Yahoo Finance API
    ticker_data = yf.Ticker(ticker)
    
    # Get historical stock price data for last 5 years
    hist = ticker_data.history(period="5y")
    
    # Calculate 7 day and 14 day moving averages
    hist['7MA'] = hist['Close'].rolling(window=7).mean()
    hist['14MA'] = hist['Close'].rolling(window=14).mean()
    
    # Calculate dynamic support and resistance levels
    hist['Resistance'] = hist['High'].rolling(window=10).max()
    hist['Support'] = hist['Low'].rolling(window=10).min()
    
    return hist

st.cache_data()
# Define functions to render each tab
def render_overview():
    # Fetch company info
    info_df,summary_text = get_company_info(ticker)

    # Render company info
    st.write(f"**{ticker} Company Information**")
    st.write("Below is some information about the company:")
    # Display the summary text
    st.write(summary_text)
    st.table(info_df)

st.cache_data()
def render_price_chart():
    # Get the stock price data
    hist = get_stock_price_data(ticker)

    # Create a candlestick chart with dynamic support and resistance levels
    fig = go.Figure()
    fig.add_trace(go.Candlestick(x=hist.index,
                                  open=hist['Open'],
                                  high=hist['High'],
                                  low=hist['Low'],
                                  close=hist['Close'],
                                  name='Price'))

    # Add dynamic support and resistance lines to the chart
    fig.add_trace(go.Scatter(x=hist.index, y=hist['Resistance'], line=dict(color='red', width=1), name='Resistance'))
    fig.add_trace(go.Scatter(x=hist.index, y=hist['Support'], line=dict(color='green', width=1), name='Support'))

    # Add 7 day and 14 day moving averages to the chart
    fig.add_trace(go.Scatter(x=hist.index,
                              y=hist['7MA'],
                              line=dict(color='orange', width=1),
                              name='7 Day Moving Average'))

    fig.add_trace(go.Scatter(x=hist.index,
                              y=hist['14MA'],
                              line=dict(color='red', width=1),
                              name='14 Day Moving Average'))

    # Update the chart layout with title and axis labels
    fig.update_layout(
        title=f"{ticker} Stock Price Chart",
        yaxis_title="Price (USD)",
        xaxis_title="Date",
        xaxis_rangeslider_visible=False
    )

    # Display the chart
    st.plotly_chart(fig)

    # Add text for price components
    st.write("Price Components:")
    st.write("- Candlestick chart displays the open, high, low, and close prices for each day.")
    st.write("- Support and resistance lines are dynamic and are calculated based on the highest high and lowest low of the previous 10 trading days.")
    st.write("- Moving averages smooth out the price data by calculating the average price over a specified time period.")

    # Add text for support and resistance
    st.write("Support and Resistance:")
    st.write("- Support is a price level where there is buying pressure, and the price is expected to bounce back up.")
    st.write("- Resistance is a price level where there is selling pressure, and the price is expected to bounce back down.")
    st.write("- Support and resistance levels can be used to identify potential buying and selling opportunities.")

    # Add text for moving averages
    st.write("Moving Averages:")
    st.write("- Moving averages are commonly used to smooth out the price data and identify trends.")
    st.write("- The 7-day and 14-day moving averages are commonly used by traders to identify short-term and long-term trends.")

st.cache_data()
def render_news():
    # Fetch news articles for the company
#     ticker = "AAPL"  # replace with your desired ticker symbol
    company = yf.Ticker(ticker)
    news_df = company.news

    news_df = pd.DataFrame(news_df)
    news_df = news_df[['title','publisher','link','providerPublishTime']]

    news_df['providerPublishTime'] = news_df['providerPublishTime'].apply(unix_time_to_datetime)

    st.table(news_df)

st.cache_data()
def render_forecasting():
    
    days_to_forecast = sidebar.slider('Select the number of days to forecast', 1, 30, 14)
    hist = get_stock_price_data(ticker)

    # Allow user to choose ARIMA or GARCH model
    model_choice = st.radio("Select a model for forecasting:", ("ARIMA", "GARCH"))

    # Prepare data for ARIMA or GARCH
    if model_choice == "ARIMA":
        df = hist[['Close']].reset_index().rename(columns={'Date': 'ds', 'Close': 'y'})
        model = auto_arima(df['y'], trace=False, error_action='ignore', suppress_warnings=True)
        forecast = model.predict(n_periods=days_to_forecast)
        model_name = "ARIMA"
        model_description = "ARIMA (Autoregressive Integrated Moving Average) is a popular time series forecasting model that uses past values to predict future values."
    else:
        df = hist['Close'].pct_change().dropna()
        model = arch_model(df, vol='GARCH', p=1, q=1)
        results = model.fit(disp='off')
        forecast = results.forecast(horizon=days_to_forecast).variance.values[-1, :]
        forecast = hist['Close'].iloc[-1] * np.exp(np.sqrt(forecast))
        model_name = "GARCH"
        model_description = "GARCH (Generalized Autoregressive Conditional Heteroskedasticity) is a popular time series forecasting model that uses past variance to predict future variance and uses that to predict future prices."

    # Create plot
    fig = go.Figure()

    # Add actual closing prices to plot
    fig.add_trace(go.Scatter(x=hist.index, y=hist['Close'], name='Actual'))

    # Add predicted values to plot
    fig.add_trace(go.Scatter(x=pd.date_range(start=hist.index[-1], periods=days_to_forecast+1, freq='D')[1:], y=forecast, name=f'{model_name} Predicted'))

    # Set plot layout
    fig.update_layout(
        title=f"{ticker} Price Forecast for next {days_to_forecast} days ({model_name})",
        xaxis_title="Date",
        yaxis_title="Price",
        legend_title="Legend",
        font=dict(
            family="Courier New, monospace",
            size=12,
            color="Black"
        )
    )

    # Show plot
    st.plotly_chart(fig)

    # Display the forecast model description
    st.write(f"**{model_name} model:** {model_description}")

    # Create a list of dates for the forecasted period
    forecast_dates = pd.date_range(start=hist.index[-1], periods=days_to_forecast+1, freq='D')[1:]

    # Create a DataFrame to store the forecasted values
    forecast_df = pd.DataFrame({'Date': forecast_dates, f'{model_name} Forecast': forecast})

    # Set the index of the DataFrame to be the Date column
    forecast_df.set_index('Date', inplace=True)

    # Display the DataFrame
    st.write(forecast_df)

# Define page layout
tabs = ['Overview', 'Price Chart', 'News','Forecasting']

# Define tabs
if 'tab' not in st.session_state:
    st.session_state.tab = 'Overview'

active_tab = tabs.index(st.session_state.tab)
tab = st.sidebar.radio('', tabs, index=active_tab)

# Define sidebar widgets
sidebar = st.sidebar
ticker = sidebar.selectbox('Select a stock', ['AAPL', 'MSFT', 'GOOG', 'AMZN'])

# Define tab contents
overview_tab = st.container()
price_chart_tab = st.container()
news_tab = st.container()
forecasting_tab = st.container()


# Show the appropriate tab
if tab == 'Overview':
    render_overview()
elif tab == 'Price Chart':
    render_price_chart()
elif tab == 'News':
    render_news()
else:
    render_forecasting()

# Save current tab in session state
st.session_state.tab = tab
