## About ES

ES is a Python based automated trading application, currently in development:

**Importer**: Data ingestion from EoD Datasource. This now covers both Sierra Charts data files and Quandl data via their API.
Pls note that sierra files need to be stored locally in the .sierra_data directory to stop Travis CI from failing during
the execution of pytests. Also

**Calculator**: Perform additional calculations on base data from importer to be able to make trade entry, exit & risk decisions.

**Trade**: Make assessments on calculated data for entry and exit criteria as well.

**Backtest**: Basic backtesting framework for trading strategies.

**Processor**: Main function for pulling Sierra file updates, running Importer, Calculator, Trade & Backtest.
Output sent to main.py.

**Main**: Flask based web application. HTML templates stored in template directory.
Static files, namely local CSS for tables held in static directory. Uses uWSGI and NGNIX in Production environment.

**test_sierra**: Basic unit, integration tests, functional and webapp tests run by pytest.
