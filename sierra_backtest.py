import logging

class Backtest:
    def __init__(self, combined):
        self.combined = combined

        # Create new logging instance
        # Log where file is ingested from
        self.logger = logging.getLogger(__name__)
        log_message = "Dataframe passed for backtest analysis"
        self.logger.debug(log_message)

    def es_vix_long_test(self):
        # Experiments to sift entire clean dataset for entry and exit criteria to look at backtesting options
        # This involved the creation of a new column time shift percentage change for the following day after a prime signal
        # This in itself will make the if/else condition in sierra_trade for condition 2 more simple.
        print("Entry(1) Criteria-------------------------------------------------------------------")
        backtest_entry_1 = self.combined[
            (self.combined['VIX_Ndt'] > 0.841) & (self.combined['VIX_Pdf'] > 0) & (self.combined['VIX_Pdf'] < 0.03)]
        print(backtest_entry_1.iloc[:, [3, 9, 12, 13, 14, 15, 18]].tail(5))
        print()

        print("Entry(2) Criteria-------------------------------------------------------------------")
        backtest_entry_2 = self.combined[
            (self.combined['VIX_NdtY'] > 0.841) & (self.combined['VIX_PdfY'] > -0.03) & (self.combined['VIX_PdfY'] < 0.03) & (
                    self.combined['VIX_Pdf'] < 0)]
        print(backtest_entry_2.iloc[:, [3, 9, 12, 13, 14, 15, 18]].tail(5))
        print()

        print("Exit(1) Criteria--------------------------------------------------------------------")
        backtest_exit = self.combined[
            (self.combined['VIX_Ndt'] < 0.159) & (self.combined['VIX_Pdf'] > -0.03) & (self.combined['VIX_Pdf'] < 0.03)]
        print(backtest_exit.iloc[:, [3, 9, 12, 13, 14, 15, 18]].tail(5))
        print()

        log_message = "Backtest completed"
        self.logger.debug(log_message)
        return