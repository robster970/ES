import logging
import boto3
from botocore.exceptions import ClientError

AWS_REGION = 'eu-west-1'


# Define main Importer class
class Messaging:
    """Class to send message notifications post trade decision calculations"""

    def __init__(self, response):

        # Create new logging instance
        self.logger = logging.getLogger(__name__)

        self.run_response = response['RunDate']
        self.last_response = response['LastEvaluated']
        self.entry_response = response['EntryDecision']
        self.exit_response = response['ExitDecision']
        self.stop_loss_response = response['StopLoss']
        self.evaluated_data_response = response['EvaluatedData']
        self.backtest_results_response = response['BacktestResult']
        self.evaluated_data_response = self.evaluated_data_response.to_html(classes='EvaluatedData')
        self.backtest_results_response = self.backtest_results_response.to_html(classes='BacktestResult')

        # Checks to ensure parameters passed in are valid
        if isinstance(response, dict):
            log_message = "Parsed response is a valid dictionary"
        else:
            raise InvalidMessagingException('Invalid dictionary: {}'.format(response))
        self.logger.debug(log_message)

        self.to = 'robster970@gmail.com'
        self.source = self.to
        self.subject = 'Trade evaluation update: ' + self.run_response
        self._html_1 = """<html>
             <head></head>
             <body>
             <p><br>Last evaluation date: """ + self.last_response + """</br>
             <br>Entry analysis: """ + self.entry_response + """</br>
             <br>Exit analysis: """ + self.exit_response + """</br>
             <br>Stop loss required: """ + str(self.stop_loss_response) + """</br>
             <br>Go to <a href='http://taplow.io'>Sierra Trading</a></br></p>
             </body>
             </html>
             """
        self._html_2 = """<html>
             <head></head>
             <body>
             <p><br> </br></p>
             </body>
             </html>
             """
        self._text = ("Unable to view html\r\n"
                      "Go to http://taplow.io"
                      )
        self._format = 'html'
        self.charset = "UTF-8"

        self.CONFIGURATION_SET = "sierra-mail"

    def ses_aws(self):
        client = boto3.client('ses', region_name=AWS_REGION)

        log_message = "SES Msg client created, sending mail"
        self.logger.debug(log_message)

        # Try to send the email.
        try:
            # Provide the contents of the email.
            response = client.send_email(
                Destination={
                    'ToAddresses': [
                        self.to,
                    ],
                },
                Message={
                    'Body': {
                        'Html': {
                            'Charset': self.charset,
                            'Data': self._html_1 + self.evaluated_data_response + self._html_2 + self.backtest_results_response,
                        },
                        'Text': {
                            'Charset': self.charset,
                            'Data': self._text,
                        },
                    },
                    'Subject': {
                        'Charset': self.charset,
                        'Data': self.subject,
                    },
                },
                Source=self.source,
                ConfigurationSetName=self.CONFIGURATION_SET,
            )
        # Log an error if something goes wrong.
        except ClientError as e:
            log_message = "Error: " + e.response['Error']['Message']
        else:
            log_message = "Email Message ID: " + response['ResponseMetadata']['RequestId']
        return log_message

# Define class for exception handling of incorrect data frame attributes
class InvalidMessagingException(Exception):
    pass