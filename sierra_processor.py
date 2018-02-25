import sierra_importer as si
import sierra_calculator as sc
import sierra_trade as st
import sierra_backtest as sb
import pandas as pd
import matplotlib.pyplot as plt
import warnings
import logging.config
import sys
import time


# Define class for exception handling in main processor
class MainSierraException(Exception):
    pass


def main_processor(source):
    # Initialise variables
    plot_output = "N"
    rolling_period = 10
    output_directory_location = '.output/'
    write_files = "N"

    # Pickup logging configuration and create logger for Processor
    logging.config.fileConfig('logging.conf')
    logger = logging.getLogger('sierra_processor')

    # Nasty way of suppressing some calculation warnings.
    # Need to find a better way of doing this.
    warnings.filterwarnings("ignore")

    # Log for start main processing
    log_message = "Processing: " + source + ". FileWrite: " + write_files + "."
    logger.info(log_message)

    # Determine how to process an import of data
    # Q is for Quandl API
    # S is for Sierra Charts text file
    if source == "Q":
        # Making a request to Quandl for ES data
        log_message = "Getting ES data from Quandl"
        logger.info(log_message)
        es = si.Importer()
        es_clean = es.get_data_quandl("CHRIS/CME_SP1", "ES")
        log_message = "ES data retrieved from Quandl"
        logger.info(log_message)

        # Making a request to Quandl for VIX data
        log_message = "Getting VIX data from Quandl"
        logger.info(log_message)
        vix = si.Importer()
        vix_clean = vix.get_data_quandl("CHRIS/CBOE_VX1", "VIX")
        log_message = "VIX data retrieved from Quandl"
        logger.info(log_message)

    elif source == "S":
        # Import ES data from a Sierra Charts txt file
        es = si.Importer()
        es_clean = es.get_data_sierra(".sierra_data/", "ESH18.dly_BarData.txt", "ES")
        log_message = "ES clean data set ready for use."
        logger.info(log_message)

        # Import VIX data from a Sierra Charts txt file
        vix = si.Importer()
        vix_clean = vix.get_data_sierra(".sierra_data/", "$VIX.dly_BarData.txt", "VIX")
        log_message = "VIX clean data set ready for use."
        logger.info(log_message)

        # Tidy up VIX data to remove last two columns for Volume and NumberOfTrades
        vix_clean = vix_clean.iloc[:, 0:4]

    else:
        raise MainSierraException('Invalid processing path for data source: {}'.format(source))

    # Create a single combined data frame to work from with the NaN rows removed
    combined = pd.concat([es_clean, vix_clean], axis=1)
    combined = combined.dropna()
    log_message = "Combined ES & VIX clean data set ready for use."
    logger.info(log_message)

    # Pass cleaned data frame to calculator for specific calculations from specific method for VIX.
    vix_calc = sc.Calculator(combined, "VIX")
    combined = vix_calc.calculate_values_vix(rolling_period)
    log_message = "Additional columns with calculations returned from calculator for VIX"
    logger.info(log_message)

    # Pass cleaned data frame to calculator for specific calculations from specific method for ES.
    es_calc = sc.Calculator(combined, "ES")
    combined = es_calc.calculate_values_es(rolling_period)
    log_message = "Additional columns with calculations returned from calculator for ES"
    logger.info(log_message)

    # Make trading entry decision for es_vix_long strategy
    log_message = "Trade entry evaluation being made"
    logger.info(log_message)
    es_decision = st.Trading(combined)
    log_message = es_decision.es_vix_long("entry")
    logger.info(log_message)

    # Make trading exit decision for es_vix_long strategy
    log_message = "Trade exit evaluation being made"
    logger.info(log_message)
    es_decision = st.Trading(combined)
    log_message = es_decision.es_vix_long("exit")
    logger.info(log_message)

    # Retrieve evaluated data for making trades using get_evaluated_data method.
    es_evaluated_data = es_decision.get_evaluated_data()
    es_stop_loss = es_decision.get_stop_loss()

    # print(es_evaluated_data)

    # Experiments to turn to JSON object but currently missing the index which isn't too hot.
    # Needs fixing.
    # print(es_evaluated_data.iloc[0].to_json(orient='index'))
    # print(es_evaluated_data.iloc[1].to_json(orient='index'))

    # Run a backtest
    es_backtest_results = sb.Backtest(combined).es_vix_long_test()
    log_message = "Backtest results returned"
    logger.info(log_message)

    # Write file outputs
    if write_files == "Y":
        orig_stdout = sys.stdout
        file_timestamp = time.strftime("%Y%m%d-%H%M%S")
        try:
            backtest_file = open(output_directory_location + source + '-' + file_timestamp + '.txt', 'w')
            source_file = open(output_directory_location + 'combined-' + file_timestamp + '.txt', 'w')
        except FileNotFoundError:
            raise MainSierraException('Invalid directory for file output: {}'.format(source))

        sys.stdout = backtest_file
        print(es_backtest_results.iloc[:, [3, 9, 12, 13, 14, 18, 19]].tail(10))
        sys.stdout = source_file
        print(combined.tail(10))
        sys.stdout = orig_stdout
        backtest_file.close()
        source_file.close()
        log_message = "Files written to: " + output_directory_location + " & timestamped: " + file_timestamp
        logger.info(log_message)
    else:
        log_message = "No output files written for source and backtest files"
        logger.info(log_message)

    print("--------------------------------------------------------------------------------")
    print(es_backtest_results.iloc[:, [3, 9, 12, 13, 14, 18, 19]].tail(10))
    print("--------------------------------------------------------------------------------")
    print("Required stop loss: " + str(es_stop_loss))
    print("--------------------------------------------------------------------------------")
    print(es_evaluated_data.tail(10))

    # Plotting the output via matplotlib.
    # Note the use is plt.ion() in conjunction with the plt.pause allows the graph to be plotted
    # using interactive and allowing the the python process to be non-blocked
    # This is finally invoked outside of the function by plt.show() in the last line of the script
    if plot_output == "Y":
        plt.ion()
        plt.figure(1)
        plt.subplot(211)
        combined['ES_Stop'].tail(20).plot(color='red')
        plt.subplot(212)
        combined['VIX_Ndt'].tail(20).plot(color='blue')
        plt.subplot(212)
        # plt.plot(combined.index, combined['ES_Stop'], 'bs', combined.index, combined['VIX_Pdf', 'g^'])
        while True:
            plt.pause(0.05)

    return


which = "S"
main_processor(which)
plt.show(block=False)
