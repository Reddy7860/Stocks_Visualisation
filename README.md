Stock Analysis App
This is a Streamlit app that provides a variety of tools for analyzing stock data. Users can select a stock, view company information, a candlestick chart of stock prices, recent news articles related to the company, and forecasted stock prices using either an ARIMA or GARCH model.

https://reddy7860-stocks-visualisation-streamlit-stocks-overview-hbcmo2.streamlit.app/

Demo
Check out the published app to see the app in action.

### Demo Video

[![Watch the video](https://img.youtube.com/vi/T-D1KVIuvjA/maxresdefault.jpg)](https://www.youtube.com/watch?v=1MLuzetP8pM)

Dependencies
This app requires the following Python libraries:

streamlit
yfinance
plotly
pandas
pmdarima
arch
Installation
To install the required Python libraries, run the following command:

bash
Copy code
pip install streamlit yfinance plotly pandas pmdarima arch
Usage
To run the app, navigate to the root directory of the project and run the following command:

bash
Copy code
streamlit run streamlit_stocks_overview.py
Once the app is running, select a stock from the dropdown menu and choose the tab corresponding to the tool you want to use. The available tabs are:

Overview: Displays information about the selected company.
Price Chart: Displays a candlestick chart of the stock's historical prices.
News: Displays recent news articles related to the selected company.
Forecasting: Uses either an ARIMA or GARCH model to forecast the stock's price for the next 1-30 days.
Contributing
If you would like to contribute to the project, feel free to submit a pull request on the GitHub repository.

License
This project is licensed under the terms of the MIT license. See the LICENSE file for details.
