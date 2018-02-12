import sierra_logger as sl
import pandas as pd


class Trading:
    """Class to make trading entry and exit decisions based upon a processed data frame being passed into the class
    for assessment"""

    def __init__(self, data_frame):
        self.data_frame = data_frame
        self.module = "sierra_trade"
        self.evaluation_frame = []

        # Create new logging instance
        # Log where file is ingested from
        importer_logger = sl.Logging()
        log_message = "Data frame passed in for trading evaluation"
        importer_logger.parser(self.module, log_message)

    def es_vix_long(self, status):

        # Build the evaluation frame and select the values of interest
        evaluation_frame = self.data_frame.tail(2)
        self.evaluation_frame = evaluation_frame

        pdf_1 = pd.to_numeric(evaluation_frame.iloc[0:1, 13])
        pdf_2 = pd.to_numeric(evaluation_frame.iloc[1:, 13])
        ndst_1 = pd.to_numeric(evaluation_frame.iloc[0:1, 12])
        ndst_2 = pd.to_numeric(evaluation_frame.iloc[1:, 12])

        # In the evaluation process below, the use of the .all() is a quirk of having to evaluate
        # a pandas dataframe which required strict boolean interpretation of comparisons.
        if status == "entry":
            response = "Entry evaluation"
            if ((ndst_2 > 0.841) & (pdf_2 > 0) & (pdf_2 < 0.03)).all():
                signal = "TRADE ACTION: Long entry confirmed on condition 1: EoD confirmation turn."
            elif ((ndst_1 > 0.841) & (pdf_1 > -0.03) & (pdf_1 < 0.03) & (pdf_2 < 0)).all():
                signal = "TRADE ACTION: Long entry confirmed on condition 2: Post EoD confirmation turn."
            else:
                signal = "NO TRADE ACTION REQUIRED: No entry conditions found"
        elif status == "exit":
            response = "Exit evaluation"
            if ((ndst_2 < 0.159) & (pdf_2 > -0.03) & (pdf_2 < 0.03)).all():
                signal = "TRADE ACTION: Long exit confirmed on condition 1: EoD confirmation to exit."
            else:
                signal = "NO TRADE ACTION REQUIRED:No exit conditions found"
        else:
            response = "Invalid status: " + status
            signal = "Invalid request made"

        importer_logger = sl.Logging()
        log_message = "Response evaluated: " + response
        importer_logger.parser(self.module, log_message)

        return signal

    def get_evaluated_data(self):
        return self.evaluation_frame
