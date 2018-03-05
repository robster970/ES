from flask import Flask, render_template
import sierra_processor

# Set webapp name to app so it can be used by NGINX docker image
# Important that filename is set to main.py also
app = Flask(__name__)


@app.route("/")
def main():
    # Set which data source and run main processor
    which = "S"
    response = sierra_processor.main_processor(which)

    # Handle the data required to render in the index.html template
    run_response = response['RunDate']
    entry_response = response['EntryDecision']
    exit_response = response['ExitDecision']
    stop_loss_response = response['StopLoss']
    evaluated_data_response = response['EvaluatedData']
    backtest_results_response = response['BacktestResult']
    evaluated_data_response = evaluated_data_response.to_html(classes='EvaluatedData')
    backtest_results_response = backtest_results_response.to_html(classes='BacktestResult')

    # Pass the variables pack into index.html fore rendering
    return render_template('index.html', source=which, run=run_response, entry=entry_response, exit=exit_response,
                           stoploss=stop_loss_response, evaluated=evaluated_data_response,
                           backtest=backtest_results_response)


# Start up the webserver
if __name__ == "__main__":
    app.run(host='0.0.0.0')
