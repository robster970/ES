import sierra_logger as sl
from scipy.stats import norm


class Calculator:
    """Class for performing additional calculations to imported and cleaned dataset to allow trading decisions to be
    made based upon the trading strategy being tested in sierra_trade"""

    def __init__(self, data_frame, column_id):
        self.data_frame = data_frame
        self.column_id = column_id
        self.module = "sierra_calculator"

        # Create new logging instance
        # Log where file is ingested from
        importer_logger = sl.Logging()
        log_message = "Data frame passed in for: " + self.column_id
        importer_logger.parser(self.module, log_message)

    def calculate_values_vix(self, rolling_period):
        # Add the new columns for calculation of VIX avg & std

        # Do the calculations for rolling average, rolling std, normdist calculation and percentage change-lagged.
        self.data_frame[self.column_id + '_Avg'] = self.data_frame[self.column_id +'_Last'].rolling(rolling_period).mean()
        self.data_frame[self.column_id + '_Std'] = self.data_frame[self.column_id +'_Last'].rolling(rolling_period).std()
        self.data_frame[self.column_id + '_Ndt'] = norm(self.data_frame[self.column_id +'_Avg'], self.data_frame[self.column_id +'_Std'])\
            .cdf(self.data_frame[self.column_id +'_Last'])
        self.data_frame[self.column_id + '_Pdf'] = self.data_frame[self.column_id +'_Last'].diff() / self.data_frame[self.column_id +'_Last']\
            .shift(1)
        self.data_frame[self.column_id + '_NdtY'] = self.data_frame[self.column_id + '_Ndt'].shift(1)
        self.data_frame[self.column_id + '_PdfY'] = self.data_frame[self.column_id + '_Pdf'].shift(1)
        # Logging statement
        importer_logger = sl.Logging()
        log_message = "Calculations performed for VIX method: " + self.column_id
        importer_logger.parser(self.module, log_message)
        return self.data_frame

    def calculate_values_es(self, rolling_period):
        # Add the new columns for calculation of ES TR, rolling ATR & Stop

        self.data_frame[self.column_id + '_Tr'] = self.data_frame[self.column_id + '_High']-self.data_frame[self.column_id +'_Low']
        self.data_frame[self.column_id + '_Atr'] = self.data_frame[self.column_id + '_Tr'].rolling(rolling_period).mean()
        self.data_frame[self.column_id + '_Stop'] = self.data_frame[self.column_id + '_Atr'] * 1.7
        return self.data_frame





