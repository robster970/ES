import logging
import pandas as pd


class Backtest:
    """Class to execute trading decisions in a backtest context"""
    def __init__(self, combined):
        self.combined = combined

        # Create new logging instance
        # Log where file is ingested from
        self.logger = logging.getLogger(__name__)
        log_message = "Dataframe passed for backtest analysis"
        self.logger.debug(log_message)

    def es_vix_long_test(self):
        # Experiments to sift entire clean dataset for entry and exit criteria to look at backtesting options
        # This involved the creation of a new column time shift percentage change for the following day after a signal
        # This in itself will make the if/else condition in sierra_trade for condition 2 more simple.
        # print("Entry(1) Criteria-------------------------------------------------------------------")
        backtest_entry_1 = self.combined[
            (self.combined['VIX_Ndt'] > 0.841) & (self.combined['VIX_Pdf'] > 0) & (self.combined['VIX_Pdf'] < 0.03)]
        backtest_entry_1['Action'] = "Entry_1"
        # print(backtest_entry_1.iloc[:, [3, 9, 12, 13, 14, 15, 18, 19]].tail(5))
        # print()

        # print("Entry(2) Criteria-------------------------------------------------------------------")
        backtest_entry_2 = self.combined[
            (self.combined['VIX_NdtY'] > 0.841) & (self.combined['VIX_PdfY'] > -0.03) & (
                        self.combined['VIX_PdfY'] < 0.03) & (
                    self.combined['VIX_Pdf'] < 0)]
        backtest_entry_2['Action'] = "Entry_2"
        # print(backtest_entry_2.iloc[:, [3, 9, 12, 13, 14, 15, 18, 19]].tail(5))
        # print()

        # print("Exit(1) Criteria--------------------------------------------------------------------")
        backtest_exit_1 = self.combined[
            (self.combined['VIX_Ndt'] < 0.159) & (self.combined['VIX_Pdf'] > -0.03) & (self.combined['VIX_Pdf'] < 0.03)]
        backtest_exit_1['Action'] = "Exit_1"
        # print(backtest_exit_1.iloc[:, [3, 9, 12, 13, 14, 15, 18, 19]].tail(5))
        # print()

        # Combine the entry and exit decisions and sort by the time-series index
        backtest_result = pd.concat([backtest_entry_1, backtest_entry_2, backtest_exit_1], axis=0)
        backtest_result.sort_index(inplace=True)

        # print(backtest_result.iloc[:, [3, 9, 12, 13, 14, 18, 19]].tail(10))

        log_message = "Backtest completed and results returned"
        self.logger.debug(log_message)
        return backtest_result
