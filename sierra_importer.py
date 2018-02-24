import pandas as pd
import quandl as qd
from quandl.errors.quandl_error import NotFoundError
import logging


# Define main Importer class
class Importer:
    """Class to import csv files generated from Sierra Charts and process into a usable time-series data-frame"""

    def __init__(self):

        # Create new logging instance
        self.logger = logging.getLogger(__name__)
        self.working_dir = ""
        self.file_name = ""
        self.column_id = ""
        self.full_path = ""
        self.data_frame = []
        self.handle = ""

    # Method to retrieve imported data
    def get_data_sierra(self, working_directory, file_name, column_id):

        # Checks to ensure parameters passed in are valid
        if isinstance(working_directory, str):
            log_message = "File location is a valid string"
            self.working_dir = working_directory
        else:
            raise InvalidFileAttributes('Invalid directory location: {}'.format(working_directory))
        self.logger.debug(log_message)

        if isinstance(file_name, str):
            log_message = "File name is a valid string"
            self.file_name = file_name
        else:
            raise InvalidFileAttributes('Invalid file name: {}'.format(file_name))
        self.logger.debug(log_message)

        if isinstance(column_id, str):
            log_message = "Column Identifier is a valid string"
            self.column_id = column_id
        else:
            raise InvalidFileAttributes('Invalid column identifier: {}'.format(column_id))
        self.logger.debug(log_message)

        # Create full path for file ingestion and log
        self.full_path = self.working_dir + self.file_name

        # Logging statement post validation
        log_message = "Ingestion and processing of: " + self.full_path
        self.logger.debug(log_message)

        # Import the file as csv into a data frame
        # Specify the headers for the data frame using the column_id
        try:
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
        except FileNotFoundError:
            # Throw error if no file can be found
            raise InvalidFileAttributes('File not found: {}'.format(self.full_path))

        # Ensure that the index is converted to a time series
        self.data_frame.index = pd.to_datetime(self.data_frame.index)

        # Logging statement to confirm creation of the object, and data frame from successful ingestion
        log_message = "Full data frame created for " + self.column_id
        self.logger.debug(log_message)

        # Reduce the data frame to just columns needed
        redacted_data = self.data_frame.iloc[:, 1:7]

        # Logging statement to confirm reduction and return

        log_message = "Redacted data frame created and data returned to requestor for " + self.column_id
        self.logger.debug(log_message)

        # Return the requested data frame from the method call
        return redacted_data

    def get_data_quandl(self, handle, column_id):

        # Checks to ensure parameters passed in are valid
        if isinstance(handle, str):
            log_message = "API handle is a valid string"
            self.handle = handle
        else:
            raise InvalidAPIAttributes('Invalid API attribute: {}'.format(handle))
        self.logger.debug(log_message)

        if isinstance(column_id, str):
            log_message = "Column ID is a valid string"
            self.column_id = column_id
        else:
            raise InvalidAPIAttributes('Invalid column ID: {}'.format(column_id))
        self.logger.debug(log_message)

        # Request data from Quandl
        log_message = "Retrieving " + self.handle + " Quandl API"
        self.logger.debug(log_message)

        try:
            self.data_frame = qd.get(self.handle, authtoken="9r5dMR3-riev4YMkjbeB")
        except NotFoundError:
            log_message = "Issue retrieving the data from Quandl API"
            self.logger.debug(log_message)
            raise InvalidAPIAttributes('Non-existent handle: {}'.format(handle))

        log_message = self.handle + " retrieved from Quandl API"
        self.logger.debug(log_message)

        if self.column_id == "ES":
            self.data_frame.columns = [self.column_id + '_Open',
                                       self.column_id + '_High',
                                       self.column_id + '_Low',
                                       self.column_id + '_Last',
                                       self.column_id + '_Change',
                                       self.column_id + '_Settle',
                                       self.column_id + '_Vol',
                                       self.column_id + '_NoT']

            self.data_frame = pd.DataFrame(self.data_frame)

            self.data_frame = self.data_frame.iloc[:, [0, 1, 2, 3, 6, 7]]

            self.data_frame[self.column_id + '_Vol'] = 0
            self.data_frame[self.column_id + '_NoT'] = 0

        elif self.column_id == "VIX":
            self.data_frame.columns = [self.column_id + '_Open',
                                       self.column_id + '_High',
                                       self.column_id + '_Low',
                                       self.column_id + '_Last',
                                       self.column_id + '_Settle',
                                       self.column_id + '_Change',
                                       self.column_id + '_Vol',
                                       self.column_id + '_EFP',
                                       self.column_id + '_OI']

            self.data_frame = pd.DataFrame(self.data_frame)

            self.data_frame = self.data_frame.iloc[:, [0, 1, 2, 3]]

        else:
            log_message = self.handle + " is not a recognised handle"
            self.logger.debug(log_message)
            raise InvalidAPIAttributes('Invalid handle passed for processing: {}'.format(column_id))

        return self.data_frame


# Define class for exception handling of incorrect file attributes
class InvalidFileAttributes(Exception):
    pass


# Define class for exception handling of incorrect API attributes
class InvalidAPIAttributes(Exception):
    pass

