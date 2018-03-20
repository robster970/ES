from flask import Flask, render_template, request
import sierra_processor
import logging


# Set webapp name to app so it can be used by NGINX docker image
# Important that filename is set to main.py also
def create_app():
    sierra_app = Flask(__name__)

    @sierra_app.route("/")
    def main():

        which = "S"
        # Set which data source and run main processor
        # Validate whether a URL parameter has been passed in using 'source'
        # Set the default to Sierra if nothing passed or it is invalid
        if 'source' in request.args:
            which = request.args['source']
            if which not in ('S', 'Q'):
                which = "S"

        response = sierra_processor.main_processor(which)

        logger = logging.getLogger('main_webserver')

        # Log for start main processing
        log_message = "Web application server rendering response"
        logger.info(log_message)

        # Handle the data required to render in the index.html template
        run_response = response['RunDate']
        last_response = response['LastEvaluated']
        entry_response = response['EntryDecision']
        exit_response = response['ExitDecision']
        stop_loss_response = response['StopLoss']
        evaluated_data_response = response['EvaluatedData']
        backtest_results_response = response['BacktestResult']
        evaluated_data_response = evaluated_data_response.to_html(classes='EvaluatedData')
        backtest_results_response = backtest_results_response.to_html(classes='BacktestResult')

        # Pass the variables pack into index.html fore rendering
        return render_template('index.html', source=which, run=run_response, last=last_response, entry=entry_response,
                               exit=exit_response, stoploss=stop_loss_response, evaluated=evaluated_data_response,
                               backtest=backtest_results_response)

    return sierra_app


# Start up the webapp
if __name__ == "__main__":
    app = create_app()
    app.run(host='0.0.0.0')
