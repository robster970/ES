from sierra_importer import Importer, InvalidFileAttributes, InvalidAPIAttributes
from sierra_calculator import Calculator, InvalidDataAttributes
import pandas as pd
import pytest
import warnings


# Nasty way of suppressing some calculation warnings.
# Need to find a better way of doing this.
warnings.filterwarnings("ignore")


#########################
# sierra_importer tests #
#########################
def test_importer_sierra_file_attributes_positive_1():
    working_directory = ".sierra_data/"
    file_name = "ESH18.dly_BarData.txt"
    column_id = "TEST"
    assert Importer().get_data_sierra(working_directory, file_name, column_id) is not None


@pytest.mark.parametrize("working_directory, file_name, column_id", [
    (3.1415, "ESH18.dly_BarData.txt", "TEST"),
    (".sierra_data/", [1, 2, 3, 4, 5], "TEST"),
    (".sierra_data/", "ESH18.dly_BarData.txt", 123.45678),
    (".sierra_data", "ESH18.dly_BarData.txt", "TEST"),
    (".sierra_data/", "ESH18.dly_BarData.t", "TEST"),

])
def test_importer_sierra_file_attributes_negative_combinations(working_directory, file_name, column_id):
    with pytest.raises(InvalidFileAttributes):
        Importer().get_data_sierra(working_directory, file_name, column_id)


@pytest.mark.parametrize("handle,  column_id", [
    ("CHRIS/CBOE_VX1", "VIX"),
    ("CHRIS/CME_SP1", "ES"),

])
def test_importer_quandl_api_attributes_positive_combinations(handle, column_id):
    assert Importer().get_data_quandl(handle, column_id) is not None


@pytest.mark.parametrize("handle,  column_id", [
    ("BE/MY_GUEST", "ES"),
    ("CHRIS/CBOE_VX1", 34567),
    ("CHRIS/CBOE_VX1", "TEST"),

])
def test_importer_quandl_api_attributes_negative_combinations(handle, column_id):
    with pytest.raises(InvalidAPIAttributes):
        Importer().get_data_quandl(handle, column_id)


###########################
# sierra_calculator tests #
###########################


@pytest.fixture()
def vix_test_object():
    column_id = "TEST"
    data = {'date': ['2014-05-01', '2014-05-02', '2014-05-03',
                     '2014-05-04', '2014-05-05', '2014-05-06',
                     '2014-05-07', '2014-05-08', '2014-05-09',
                     '2014-05-10'],
            column_id + '_High': [1934, 1925, 1926, 1915, 1915, 1914, 1926, 1925, 1962, 1941],
            column_id + '_Last': [1920, 1910, 1905, 1900, 1890, 1880, 1905, 1903, 1930, 1920]}
    data_frame = pd.DataFrame(data, columns=['date', column_id + '_High', column_id + '_Last'])
    # Ensure that the index is converted to a time series
    data_frame.index = pd.to_datetime(data_frame['date'])
    # Drop the duplicated date
    data_frame.drop('date', axis=1, inplace=True)
    return data_frame


def test_calculator_data_attributes_positive():
    column_id = "TEST"
    assert Calculator(vix_test_object(), column_id)


def test_calculator_data_attributes_negative_1():
    column_id = "TEST"
    data_frame = [1, 2, 3, 4, 5]
    with pytest.raises(InvalidDataAttributes):
        Calculator(data_frame, column_id)


def test_calculator_data_attributes_negative_2():
    column_id = 123
    with pytest.raises(InvalidDataAttributes):
        Calculator(vix_test_object(), column_id)


def test_calculator_calculate_vix_values():
    rolling_period = 3
    column_id = "TEST"
    test_object = Calculator(vix_test_object(), column_id)
    assert test_object.calculate_values_vix(rolling_period) is not None


def test_calculator_calculate_vix_values_negative_1():
    rolling_period = "Yes"
    column_id = "TEST"
    test_object = Calculator(vix_test_object(), column_id)
    with pytest.raises(InvalidDataAttributes):
        test_object.calculate_values_vix(rolling_period)


@pytest.fixture()
def es_test_object():
    column_id = "TEST"
    data = {'date': ['2014-05-01', '2014-05-02', '2014-05-03',
                     '2014-05-04', '2014-05-05', '2014-05-06',
                     '2014-05-07', '2014-05-08', '2014-05-09',
                     '2014-05-10'],
            column_id + '_High': [1934, 1925, 1926, 1915, 1915, 1914, 1926, 1925, 1962, 1941],
            column_id + '_Low': [1920, 1910, 1905, 1900, 1890, 1880, 1905, 1903, 1930, 1920]}
    data_frame = pd.DataFrame(data, columns=['date', column_id + '_High', column_id + '_Low'])
    # Ensure that the index is converted to a time series
    data_frame.index = pd.to_datetime(data_frame['date'])
    # Drop the duplicated date
    data_frame.drop('date', axis=1, inplace=True)
    return Calculator(data_frame, column_id)


def test_calculator_calculate_es_values():
    rolling_period = 3
    assert es_test_object().calculate_values_es(rolling_period) is not None


def test_calculator_calculate_es_values_negative_1():
    rolling_period = "Yes"
    with pytest.raises(InvalidDataAttributes):
        es_test_object().calculate_values_es(rolling_period)
