import pandas as pd
import logger


class Importer:
    """Class to import csv files generated from Sierra Charts and process into a usable time-series dataframe"""

    def __init__(self, working_directory, file_name, column_id):
        self.working_dir = working_directory
        self.file_name = file_name
        self.full_path = self.working_dir + self.file_name
        self.column_id = column_id
        self.module = "sierra_importer"

        # Create new logging instance
        # Log where file is ingested from
        importer_logger = logger.Logging()
        log_message = "File location for import: " + self.full_path
        importer_logger.parser(self.module, log_message)

        # Import the file as csv into a dataframe
        # Specify the headers for the dataframe using the column_id
        # Ensure that the index is converted to a time series
        self.data_frame = pd.read_csv(self.full_path,
                                      header=0,
                                      names=['Date',
                                             self.column_id + '_Time',
                                             self.column_id + '_Open',
                                             self.column_id + '_High',
                                             self.column_id + '_Low',
                                             self.column_id + '_Last',
                                             self.column_id + '_Vol',
                                             self.column_id + '_NoT',
                                             self.column_id + '_Bid',
                                             self.column_id + '_Ask'],
                                      index_col=0)
        self.data_frame.index = pd.to_datetime(self.data_frame.index)
        log_message = "Full data frame created for " + self.column_id
        importer_logger.parser(self.module, log_message)

    def get_data(self):
        # Method to retrieve imported data
        redacted_data = self.data_frame.iloc[:, 1:7]
        log_message = "Redacted data frame created and data returned to requestor for " + self.column_id
        importer_logger = logger.Logging()
        importer_logger.parser(self.module, log_message)
        return redacted_data
