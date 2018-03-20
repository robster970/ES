import logging

# Define main Importer class
class Messaging:
    """Class to send messages post trade decision calculations"""

    def __init__(self, response):

        # Create new logging instance
        self.logger = logging.getLogger(__name__)

        self.response = response

    def ses_aws(self):
            return "Message sent to AWS SES"
