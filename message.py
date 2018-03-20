import sierra_processor
import sierra_messaging as sm
import logging


# Define class for exception handling in main processor
class MainMessagingException(Exception):
    pass


# Set the data source - this needs to be done in code
# as there is currently no way of setting this in an accessible way
which = 'S'

# Run main sierra_processor to get data for message
response = sierra_processor.main_processor(which)

# Start logger
logger = logging.getLogger('main_messenger')

# Log for starting main messaging processing
log_message = "Messaging service started"
logger.info(log_message)

# Create and send a new message
new_message = sm.Messaging(response)
message_response = new_message.ses_aws()
log_message = "New message handled: " + message_response
logger.info(log_message)
