## About ES

ES is a Python based automated trading application, currently in development:

**Importer**: Data ingestion currently from output of EoD data from Sierra Charts, to be converted to real time data feed.
This now covers both Sierra Charts data files and Quandl data via their API.
Pls note that sierra files need to be stored locally in the .sierra_data directory to stop Travis CI from failing during
the execution of pytests.

**Calculator**: Perform additional calculations on base data from importer to be able to make trade entry, exit & risk decisions.

**Trade**: Make assessments on calculated data for entry and exit criteria as well.

**Backtest**: Basic backtesting framework for trading strategies.

**Processor**: Main execution process.

**test_sierra**: Basic unit and integration tests.
