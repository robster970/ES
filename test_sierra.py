from sierra_importer import Importer, InvalidFileAttributes, InvalidAPIAttributes
from sierra_calculator import Calculator, InvalidDataAttributes
from sierra_processor import main_processor, MainSierraException
from sierra_trade import Trading, InvalidTradeAttributes
from sierra_backtest import Backtest, InvalidBacktestAttributes
import pandas as pd
import pytest
import warnings


# Nasty way of suppressing some calculation warnings.
# Need to find a better way of doing this.
warnings.filterwarnings("ignore")


##########################
# sierra_processor tests #
##########################
@pytest.mark.parametrize("source", [
    "Q",
    "S",
    "A"

])
def test_processor_attributes_positive_combinations(source):
    try:
        main_processor(source)
    except MainSierraException:
        print("MainSierraException invoked correctly")


def test_processor_attributes_negative_1():
    with pytest.raises(MainSierraException):
        source = "A"
        main_processor(source)


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


###########################
# sierra_trade tests      #
###########################
@pytest.fixture()
def combined_test_object():
    es = Importer()
    es_clean = es.get_data_sierra(".sierra_data/", "ESH18.dly_BarData.txt", "ES")
    vix = Importer()
    vix_clean = vix.get_data_sierra(".sierra_data/", "$VIX.dly_BarData.txt", "VIX")
    vix_clean = vix_clean.iloc[:, 0:4]
    combined = pd.concat([es_clean, vix_clean], axis=1)
    combined = combined.dropna()
    vix_column_id = "VIX"
    es_column_id = "ES"
    rolling_period = 10
    vix_input = Calculator(combined, vix_column_id)
    combined = vix_input.calculate_values_vix(rolling_period)
    es_input = Calculator(combined, es_column_id)
    combined = es_input.calculate_values_es(rolling_period)
    return combined


def test_trade_data_attributes_positive():
    assert Trading(combined_test_object()) is not None


def test_trade_data_attributes_negative_1():
    bad_dataframe = [1, 3, 5, 7, 9]
    with pytest.raises(InvalidTradeAttributes):
        Trading(bad_dataframe)


@pytest.mark.parametrize("status", [
    "entry",
    "exit",
    "Brexit",
    3.1415,

])
def test_trade_processor_type_positive_combinations(status):
    try:
        f = combined_test_object()
        g = Trading(f)
        assert g.es_vix_long(status).find("TRADE ACTION")
    except InvalidTradeAttributes:
        print("InvalidTradeAttributes exception invoked")


def test_trade_processor_type_negative_1():
    f = combined_test_object()
    g = Trading(f)
    with pytest.raises(InvalidTradeAttributes):
        g.es_vix_long('Brexit')


def test_trade_processor_get_data_positive():
    f = combined_test_object()
    g = Trading(f)
    g.es_vix_long("entry")
    assert g.get_evaluated_data() is not None


def test_trade_processor_get_stop_positive():
    f = combined_test_object()
    g = Trading(f)
    g.es_vix_long("entry")
    assert isinstance(g.get_stop_loss(), (int, float))


###########################
# sierra_trade tests      #
###########################
def test_backtest_data_attributes_positive():
    assert Backtest(combined_test_object()).es_vix_long_test() is not None


def test_backtest_data_attributes_negative():
    data_frame = [1, 2, 3, 4, 5]
    with pytest.raises(InvalidBacktestAttributes):
        Backtest(data_frame).es_vix_long_test()
