import sierra_importer as si
import sierra_calculator as sc
import sierra_logger as sl
import sierra_trade as st
import pandas as pd
import matplotlib.pyplot as plt
import warnings

# Nasty way of suppressing some calculation warnings.
# Need to find a better way of doing this.
warnings.filterwarnings("ignore")

# Set up logger
processor_logger = sl.Logging()
module = "sierra_processor"
log_message = "Processing started"
processor_logger.parser(module, log_message)

# Import ES data
es = si.Importer("/home/robster970/repo/e-mini/sierrafiles/", "ESH18.dly_BarData.txt", "ES")
es_clean = es.get_data()
log_message = "ES clean data set ready for use."
processor_logger.parser(module, log_message)

# Import VIX data
vix = si.Importer("/home/robster970/repo/e-mini/sierrafiles/", "$VIX.dly_BarData.txt", "VIX")
vix_clean = vix.get_data()
log_message = "VIX clean data set ready for use."
processor_logger.parser(module, log_message)

# Tidy up VIX data to remove last two columns for volume and NumberOfTrades
vix_clean = vix_clean.iloc[:, 0:4]

# Create a single combined data frame to work from with NaN rows removed
combined = pd.concat([es_clean, vix_clean], axis=1)
combined = combined.dropna()
log_message = "Combined ES & VIX clean data set ready for use."
processor_logger.parser(module, log_message)

# Pass cleaned data frame to calculator for specific calculations from specific method for VIX.
vix_calc = sc.Calculator(combined, "VIX")
combined = vix_calc.calculate_values_vix(10)
log_message = "Additional columns with calculations returned from calculator VIX"
processor_logger.parser(module, log_message)

# Pass cleaned data frame to calculator for specific calculations from specific method for VIX.
es_calc = sc.Calculator(combined, "ES")
combined = es_calc.calculate_values_es(10)
log_message = "Additional columns with calculations returned from calculator for ES"
processor_logger.parser(module, log_message)

# Make trading entry decision foe es_vix_long strategy
es_decision = st.Trading(combined)
log_message = es_decision.es_vix_long("entry")
processor_logger.parser(module, log_message)

# Make trading exit decision foe es_vix_long strategy
es_decision = st.Trading(combined)
log_message = es_decision.es_vix_long("exit")
processor_logger.parser(module, log_message)

# Retrieve evaluated data for making trades using get_evaluated_data method.
es_evaluated_data = es_decision.get_evaluated_data()
print("-------------------------------------------------------------------------")
print(es_evaluated_data)
print("-------------------------------------------------------------------------")

# Experiments to turn to JSON object but currently missing the index which isn't too hot.
# Needs fixing.
#print(es_evaluated_data.iloc[0].to_json(orient='index'))
#print(es_evaluated_data.iloc[1].to_json(orient='index'))

# Experiments to sift entire clean dataset for entry and exit criteria to look at backtesting options
# This involved the creation of a new column time shift percentage change for the following day after a prime signal
# This in itself will make the if/else condition in sierra_trade for condition 2 more simple.
# backtest_entry_1 = combined[(combined['VIX_Ndt'] > 0.841) & (combined['VIX_Pdf'] > 0) & (combined['VIX_Pdf'] < 0.03)]
# backtest_entry_2 = combined[(combined['VIX_NdtY'] > 0.841) & (combined['VIX_PdfY'] > -0.03) & (combined['VIX_PdfY'] < 0.03) & (combined['VIX_Pdf'] < 0)]
# backtest_exit = combined[(combined['VIX_Ndt'] < 0.159) & (combined['VIX_Pdf'] > -0.03) & (combined['VIX_Pdf'] < 0.03)]
# print(backtest_entry_1.iloc[:,[3,9,12,13,14,15]].tail(5))
# print(backtest_entry_2.iloc[:,[3,9,12,13,14,15]].tail(5))
# print(backtest_exit.iloc[:,[3,9,12,13,14,15]].tail(5))

#combined['VIX_Ndt'].tail(20).plot(color='red')
#plt.show()
#combined['VIX_Pdf'].tail(20).plot(color='blue')
#plt.show()
