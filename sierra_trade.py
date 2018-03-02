import pandas as pd
import logging


class Trading:
    """Class to make trading entry and exit decisions based upon a processed data frame being passed into the class
    for assessment"""

    def __init__(self, data_frame):

        # Create new logging instance
        self.logger = logging.getLogger(__name__)

        self.stop = 0
        self.evaluation_frame = {}
        self.data_frame = {}
        self.signal = ''
        self.response = ''

        # Checks to ensure parameters passed in are valid
        if isinstance(data_frame, pd.DataFrame):
            log_message = "Data frame is a valid pandas dataframe"
            self.data_frame = data_frame
        else:
            raise InvalidTradeAttributes('Invalid pandas dataframe: {}'.format(data_frame))
        self.logger.debug(log_message)

    def es_vix_long(self, status):

        if isinstance(status, str):
            if status == 'entry' or status == 'exit':
                log_message = "Status is a valid string"
                self.logger.debug(log_message)
            else:
                raise InvalidTradeAttributes('Invalid status identifier: {}'.format(status))

        # Build the evaluation frame and select the values of interest
        self.evaluation_frame = self.data_frame.tail(2)

        pdf_1 = pd.to_numeric(self.evaluation_frame.iloc[0:1, 13])
        pdf_2 = pd.to_numeric(self.evaluation_frame.iloc[1:, 13])
        ndst_1 = pd.to_numeric(self.evaluation_frame.iloc[0:1, 12])
        ndst_2 = pd.to_numeric(self.evaluation_frame.iloc[1:, 12])
        stop_1 = pd.to_numeric(self.evaluation_frame.iloc[0:1, 18])
        stop_2 = pd.to_numeric(self.evaluation_frame.iloc[1:, 18])

        # In the evaluation process below, the use of the .all() is a quirk of having to evaluate
        # a pandas dataframe which required strict boolean interpretation of comparisons.
        if status == "entry":
            self.response = "Entry evaluation"
            if ((ndst_2 > 0.841) & (pdf_2 > 0) & (pdf_2 < 0.03)).all():
                self.signal = "TRADE ACTION: Long entry confirmed on condition 1: EoD confirmation turn."
                self.stop = stop_1
            elif ((ndst_1 > 0.841) & (pdf_1 > -0.03) & (pdf_1 < 0.03) & (pdf_2 < 0)).all():
                self.signal = "TRADE ACTION: Long entry confirmed on condition 2: Post EoD confirmation turn."
                self.stop = stop_2
            else:
                self.signal = "NO ACTION REQUIRED: No entry conditions found"
        elif status == "exit":
            self.response = "Exit evaluation"
            if ((ndst_2 < 0.159) & (pdf_2 > -0.03) & (pdf_2 < 0.03)).all():
                self.signal = "TRADE ACTION: Long exit confirmed on condition 1: EoD confirmation to exit."
            else:
                self.signal = "NO ACTION REQUIRED: No exit conditions found"
        else:
            raise InvalidTradeAttributes('Invalid status identifier: {}'.format(status))

        log_message = "Response evaluated: " + self.response
        self.logger.debug(log_message)

        return self.signal

    def get_evaluated_data(self):
        return self.evaluation_frame

    def get_stop_loss(self):
        return self.stop


# Define class for exception handling of incorrect data frame attributes
class InvalidTradeAttributes(Exception):
    pass
