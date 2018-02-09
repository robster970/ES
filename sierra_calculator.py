import sierra_logger as sl
from scipy.stats import norm


class Calculator:

    def __init__(self, data_frame, column_id):
        self.data_frame = data_frame
        self.column_id = column_id
        self.module = "sierra_calculator"

        # Create new logging instance
        # Log where file is ingested from
        importer_logger = sl.Logging()
        log_message = "Data frame passed in for: " + self.column_id
        importer_logger.parser(self.module, log_message)

    def calculate_values_VIX(self, rolling_period):
        # Add the new columns for calculation of VIX avg & std
        self.rolling_period = rolling_period

        # Do the calculations for rolling average, rolling std, normdist calculation and percentage change-lagged.
        self.data_frame[self.column_id + '_Avg'] = self.data_frame['VIX_Last'].rolling(self.rolling_period).mean()
        self.data_frame[self.column_id + '_Std'] = self.data_frame['VIX_Last'].rolling(self.rolling_period).std()
        self.data_frame[self.column_id + '_Ndt'] = norm(self.data_frame['VIX_Avg'], self.data_frame['VIX_Std'])\
            .cdf(self.data_frame['VIX_Last'])
        self.data_frame[self.column_id + '_Pdf'] = self.data_frame['VIX_Last'].diff() / self.data_frame['VIX_Last']\
            .shift(1)
        # Logging statement
        importer_logger = sl.Logging()
        log_message = "Calculations performed for VIX method: " + self.column_id
        importer_logger.parser(self.module, log_message)
        return self.data_frame
