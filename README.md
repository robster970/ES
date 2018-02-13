## About ES

ES is a Python based automated trading application, currently in development:

Importer: Data ingestion currently from output of EoD data from Sierra Charts, to be converted to real time data feed.

Logger: Basic logging, currently written to console but eventually to be written to log file in S3.

Calculator: Perform additional calculations on base data from importer to be able to make trade entry, exit & risk decisions.

Trade: Make assessments on calculated data for entry and exit criteria as well.

Backtest: Basic backtesting framework for trading strategies.

Processor: Main execution process.
