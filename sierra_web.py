from flask import Flask, render_template
import sierra_processor

sierra_web = Flask(__name__)


@sierra_web.route("/")
def main():
    which = "Q"
    response = sierra_processor.main_processor(which)
    run_response = response['RunDate']
    entry_response = response['EntryDecision']
    exit_response = response['ExitDecision']
    stop_loss_response = response['StopLoss']
    evaluated_data_response = response['EvaluatedData']
    backtest_results_response = response['BacktestResult']

    return render_template('index.html', source=which, run=run_response, entry=entry_response, exit=exit_response,
                           stoploss=stop_loss_response, evaluated=evaluated_data_response,
                           backtest=backtest_results_response)


if __name__ == "__main__":
    sierra_web.run()
