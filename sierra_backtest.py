import pandas as pd
import logging


class Backtest:
    """Class to execute trading decisions in a backtest context"""

    def __init__(self, combined):

        # Create new logging instance
        self.logger = logging.getLogger(__name__)

        self.combined = combined

        # Checks to ensure parameters passed in are valid
        if isinstance(combined, pd.DataFrame):
            log_message = "Data frame is a valid pandas dataframe"
            self.combined = combined
        else:
            raise InvalidBacktestAttributes('Invalid pandas dataframe: {}'.format(combined))
        self.logger.debug(log_message)

    def es_vix_long_test(self):
        # Experiments to sift entire clean dataset for entry and exit criteria to look at backtesting options
        # This involved the creation of a new column time shift percentage change for the following day after a signal
        # This in itself will make the if/else condition in sierra_trade for condition 2 more simple.
        # print("Entry(1) Criteria-------------------------------------------------------------------")
        backtest_entry_1 = self.combined[
            (self.combined['VIX_Ndt'] > 0.841) & (self.combined['VIX_Pdf'] > 0) & (self.combined['VIX_Pdf'] < 0.03)]
        backtest_entry_1['Action'] = "Entry_1"
        backtest_entry_2 = self.combined[
            (self.combined['VIX_NdtY'] > 0.841) & (self.combined['VIX_PdfY'] > -0.03) & (
                        self.combined['VIX_PdfY'] < 0.03) & (
                    self.combined['VIX_Pdf'] < 0)]
        backtest_entry_2['Action'] = "Entry_2"
        backtest_exit_1 = self.combined[
            (self.combined['VIX_Ndt'] < 0.159) & (self.combined['VIX_Pdf'] > -0.03) & (self.combined['VIX_Pdf'] < 0.03)]
        backtest_exit_1['Action'] = "Exit_1"

        # Combine the entry and exit decisions and sort by the time-series index
        backtest_result = pd.concat([backtest_entry_1, backtest_entry_2, backtest_exit_1], axis=0)
        backtest_result.sort_index(inplace=True)

        log_message = "Backtest completed and results returned"
        self.logger.debug(log_message)
        return backtest_result


# Define class for exception handling of incorrect data frame attributes
class InvalidBacktestAttributes(Exception):
    pass
