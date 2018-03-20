## About ES

ES is a Python based automated trading application, currently in development, consisting of a number of modules:

**Sierra Importer**: Data ingestion from EoD Datasource. This now covers both Sierra Charts data files and Quandl data via their API.
Pls note that sierra files need to be stored locally in the .sierra_data directory to stop Travis CI from failing during
the execution of pytests.

**Sierra Calculator**: Perform additional calculations on base data from importer to be able to make trade entry, exit & risk decisions.

**Sierra Trade**: Make assessments on calculated data for entry and exit criteria. Calculates risk.

**Sierra Backtest**: Basic backtesting framework to run trading strategies retrospectively.

**Sierra Messaging**: Module used for sending notifications via e-mail, initially configured to use AWS SES.

**Sierra Processor**: Main orchestration function for pulling Sierra file updates, running Importer, Calculator, Trade & Backtest.

**Main**: Flask based web application which calls Sierra Processor and renders results to a browser. HTML templates stored in template directory.
Static files, namely local CSS for tables held in static directory.

**Message**: Small script which calls Sierra Processor and passes results to Sierra Messaging as an alternative way of getting trade
evaluation results as opposed to using a browser. Designed to run under crontab offline.

All modules are packed up into a Docker container which also incorporates uWSGI app server and NGINX reverse proxy/webserver
for production deployment.


**test_sierra**: Basic unit, integration tests, functional and web application tests which can be run locally or in a CI environment.


