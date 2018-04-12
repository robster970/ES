from flask import Flask, render_template, request
from apscheduler.schedulers.background import BackgroundScheduler
import sierra_processor as sp
import sierra_messaging as sm
import logging
import yaml
import requests_cache


# Load basic config for Flask application
config = yaml.safe_load(open("webserver_config.yml"))
default_host = config['default_host']
default_port = config['default_port']
default_debug = config['default_debug']

# Start the URL request cache up and make sure it is cleared on start-up
requests_cache.install_cache(cache_name='sierra_cache', backend='memory')
requests_cache.clear()


# Create the notification function used by the scheduler
def message_notification():
    # Set the data source - this needs to be done in code, local scope applies
    # as there is currently no way of setting this in an accessible way
    which = 'S'
    source = 'robster970@gmail.com'
    write_files = 'N'

    # Clear URL request cache so that stale data is not kept
    # once all the updates have been completed
    requests_cache.clear()

    # Run main sierra_processor to get data for message
    response = sp.main_processor(which, write_files)

    # Start logger
    logger = logging.getLogger('main_messenger')

    # Log for starting main messaging processing
    log_message = "Scheduled messaging service started"
    logger.info(log_message)

    # Create and send a new message
    message_response = sm.Messaging(response, source).ses_aws()
    log_message = "Message service response: " + message_response
    logger.info(log_message)

    # Log for message confirming clearing of cache
    log_message = "URL cache cleared"
    logger.info(log_message)

    return "Email notification sent"


# Set webapp name to app so it can be used by NGINX docker image
# Important that filename is set to main.py also
def create_app():
    # init the flask object
    sierra_app = Flask(__name__)

    # Create a message scheduler to run in the background and start it
    sierra_scheduler = BackgroundScheduler()
    sierra_scheduler.start()

    # Set up the scheduler to use the messaging function using a cron like schedule
    sierra_scheduler.add_job(message_notification, 'cron', day_of_week='mon-fri', hour=22, minute=45)

    # Define URLs and associated processing
    @sierra_app.route("/")
    def main():

        # Set which data source and run main processor
        # Validate whether a URL parameter has been passed in using 'source'
        # Set the default to Sierra if nothing passed or it is invalid
        which = "S"
        write_files = 'N'
        if 'source' in request.args:
            which = request.args['source']
            if which not in ('S', 'Q'):
                which = "S"

        # Run the processor
        response = sp.main_processor(which, write_files)

        # Handle the data required to render in index.html template
        run_response = response['RunDate']
        last_response = response['LastEvaluated']
        entry_response = response['EntryDecision']
        exit_response = response['ExitDecision']
        stop_loss_response = response['StopLoss']
        evaluated_data_response = response['EvaluatedData']
        backtest_results_response = response['BacktestResult']
        evaluated_data_response = evaluated_data_response.to_html(classes='EvaluatedData')
        backtest_results_response = backtest_results_response.to_html(classes='BacktestResult')
        mikes_mood_response = response['MikesMood']

        # Pass the variables pack into index.html for rendering
        return render_template('index.html', source=which, run=run_response, last=last_response, entry=entry_response,
                               exit=exit_response, stoploss=stop_loss_response, evaluated=evaluated_data_response,
                               backtest=backtest_results_response, mikesmood=mikes_mood_response)

    # @sierra_app.route("/scheduler")
    # def scheduler():
    #     which = "S"
    #     write_files = "N"
    #     response = sp.main_processor(which, write_files)
    #     sm.Messaging(response, "robster970@gmail.com").ses_aws()
    #     return "Message was sent! Check your mail."

    return sierra_app


# Start up the flask app
if __name__ == "__main__":
    app = create_app()
    app.run(host=default_host, debug=default_debug, port=default_port)
