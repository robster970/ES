from sierra_importer import Importer, InvalidFileAttributes
from sierra_calculator import Calculator, InvalidDataAttributes
import pandas as pd
import pytest


# sierra_importer tests
def test_importer_file_attributes_positive_1():
    working_directory = "/home/robster970/repo/e-mini/sierrafiles/"
    file_name = "ESH18.dly_BarData.txt"
    column_id = "TEST"
    assert Importer(working_directory, file_name, column_id)


def test_importer_file_attributes_negative_1():
    working_directory = 24.6784
    file_name = "ESH18.dly_BarData.txt"
    column_id = "TEST"
    with pytest.raises(InvalidFileAttributes):
        Importer(working_directory, file_name, column_id)


def test_importer_file_attributes_negative_2():
    working_directory = "/home/robster970/repo/e-mini/sierrafiles/"
    file_name = [1, 2, 3, 4, 5]
    column_id = "TEST"
    with pytest.raises(InvalidFileAttributes):
        Importer(working_directory, file_name, column_id)


def test_importer_file_attributes_negative_3():
    working_directory = "/home/robster970/repo/e-mini/sierrafiles/"
    file_name = "ESH18.dly_BarData.txt"
    column_id = 123.45678
    with pytest.raises(InvalidFileAttributes):
        Importer(working_directory, file_name, column_id)


def test_importer_get_data_1():
    working_directory = "/home/robster970/repo/e-mini/sierrafiles/"
    file_name = "ESH18.dly_BarData.txt"
    column_id = "ES"
    test_object = Importer(working_directory, file_name, column_id)
    assert test_object.get_data() is not None


# sierra_calculator tests
def test_calculator_file_attributes_positive():
    column_id = "TEST"
    data = {'date': ['2014-05-01', '2014-05-02', '2014-05-03',
                     '2014-05-04', '2014-05-05', '2014-05-06',
                     '2014-05-07', '2014-05-08', '2014-05-09',
                     '2014-05-10'],
            column_id + '_High': [1934, 1925, 1926, 1915, 1915, 1914, 1926, 1925, 1962, 1941]}
    data_frame = pd.DataFrame(data, columns=['date', column_id + '_High'])
    # Ensure that the index is converted to a time series
    data_frame.index = pd.to_datetime(data_frame['date'])
    # Drop the duplicated date
    data_frame.drop('date', axis=1, inplace=True)
    assert Calculator(data_frame, column_id)


def test_calculator_file_attributes_negative_1():
    column_id = "TEST"
    data_frame = [1, 2, 3, 4, 5]
    with pytest.raises(InvalidDataAttributes):
        Calculator(data_frame, column_id)


def test_calculator_file_attributes_negative_2():
    column_id = 123
    data = {'date': ['2014-05-01', '2014-05-02', '2014-05-03',
                     '2014-05-04', '2014-05-05', '2014-05-06',
                     '2014-05-07', '2014-05-08', '2014-05-09',
                     '2014-05-10'],
            'TEST_High': [1934, 1925, 1926, 1915, 1915, 1914, 1926, 1925, 1962, 1941]}
    data_frame = pd.DataFrame(data, columns=['date', 'TEST_High'])
    # Ensure that the index is converted to a time series
    data_frame.index = pd.to_datetime(data_frame['date'])
    # Drop the duplicated date
    data_frame.drop('date', axis=1, inplace=True)
    with pytest.raises(InvalidDataAttributes):
        Calculator(data_frame, column_id)
