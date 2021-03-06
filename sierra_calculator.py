from scipy.stats import norm
import pandas as pd
import logging


class Calculator:
    """Class for performing additional calculations to imported and cleaned data-sets to allow trading decisions to be
    made based upon the trading strategy being tested in sierra_trade"""

    def __init__(self, data_frame, column_id):

        # Create new logging instance
        self.logger = logging.getLogger(__name__)

        # Checks to ensure parameters passed in are valid
        if isinstance(data_frame, pd.DataFrame):
            log_message = "Data frame is a valid pandas dataframe"
            self.data_frame = data_frame
        else:
            raise InvalidDataAttributes('Invalid pandas dataframe: {}'.format(data_frame))
        self.logger.debug(log_message)

        if isinstance(column_id, str):
            log_message = "Column Identifier is a valid string"
            self.column_id = column_id
        else:
            raise InvalidDataAttributes('Invalid column identifier: {}'.format(column_id))
        self.logger.debug(log_message)

        # Log where file is ingested from
        log_message = "Data frame passed in for: " + self.column_id
        self.logger.debug(log_message)

    # Method to calculate necessary values for VIX
    def calculate_values_vix(self, rolling_period):

        # Check to see that params passed are valid
        if isinstance(rolling_period, int):
            log_message = "Rolling period is a valid integer"
        else:
            raise InvalidDataAttributes('Invalid rolling period: {}'.format(rolling_period))
        self.logger.debug(log_message)

        # Add the new columns for calculation of VIX avg & std
        # Do the calculations for rolling average, rolling std, normdist calculation and percentage change-lagged.
        self.data_frame[self.column_id + '_Avg'] = self.data_frame[self.column_id + '_Last'].rolling(
            rolling_period).mean()

        self.data_frame[self.column_id + '_Std'] = self.data_frame[self.column_id + '_Last'].rolling(
            rolling_period).std()

        self.data_frame[self.column_id + '_Ndt'] = norm(self.data_frame[self.column_id + '_Avg'],
                                                        self.data_frame[self.column_id + '_Std']) \
            .cdf(self.data_frame[self.column_id + '_Last'])

        self.data_frame[self.column_id + '_Pdf'] = self.data_frame[self.column_id + '_Last'].diff() / self.data_frame[
            self.column_id + '_Last'] \
            .shift(1)

        self.data_frame[self.column_id + '_NdtY'] = self.data_frame[self.column_id + '_Ndt'].shift(1)

        self.data_frame[self.column_id + '_PdfY'] = self.data_frame[self.column_id + '_Pdf'].shift(1)

        # Logging statement post calculations
        log_message = "Calculations performed for VIX method: " + self.column_id
        self.logger.debug(log_message)

        # Return the data from the method call.
        return self.data_frame

    # Method to calculate necessary values for ES
    def calculate_values_es(self, rolling_period):

        # Check to see that params passed are valid
        if isinstance(rolling_period, int):
            log_message = "Rolling period is a valid integer"
        else:
            raise InvalidDataAttributes('Invalid rolling period: {}'.format(rolling_period))
        self.logger.debug(log_message)

        # Add the new columns for calculation of ES TR, rolling ATR & Stop
        # Do the calculations for TR a rolling ATR and a Stop which is a factor of ATR.

        stop_factor = 1.7

        self.data_frame[self.column_id + '_Tr'] = self.data_frame[self.column_id + '_High'] - self.data_frame[
            self.column_id + '_Low']

        self.data_frame[self.column_id + '_Atr'] = self.data_frame[self.column_id + '_Tr'].rolling(
            rolling_period).mean()

        self.data_frame[self.column_id + '_Stop'] = self.data_frame[self.column_id + '_Atr'] * stop_factor

        # Logging statement post calculations
        log_message = "Calculations performed for ES method: " + self.column_id
        self.logger.debug(log_message)

        # Return data from method call
        return self.data_frame


# Define class for exception handling of incorrect data frame attributes
class InvalidDataAttributes(Exception):
    pass
