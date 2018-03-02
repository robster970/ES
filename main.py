from flask import Flask, render_template
import sierra_processor

app = Flask(__name__)


@app.route("/")
def main():
    which = "S"
    response = sierra_processor.main_processor(which)
    run_response = response['RunDate']
    entry_response = response['EntryDecision']
    exit_response = response['ExitDecision']
    stop_loss_response = response['StopLoss']
    evaluated_data_response = response['EvaluatedData']
    backtest_results_response = response['BacktestResult']
    evaluated_data_response = evaluated_data_response.to_html(classes='EvaluatedData')
    backtest_results_response = backtest_results_response.to_html(classes='BacktestResult')

    return render_template('index.html', source=which, run=run_response, entry=entry_response, exit=exit_response,
                           stoploss=stop_loss_response, evaluated=evaluated_data_response,
                           backtest=backtest_results_response)


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
