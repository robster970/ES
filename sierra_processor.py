import sierra_importer as si
import sierra_calculator as sc
import sierra_trade as st
import sierra_backtest as sb
import pandas as pd
import matplotlib.pyplot as plt
import warnings
import logging.config

logging.config.fileConfig('logging.conf')
logger = logging.getLogger('sierra_processor')

# Nasty way of suppressing some calculation warnings.
# Need to find a better way of doing this.
warnings.filterwarnings("ignore")

# Set up logger
log_message = "Processing started"
logger.info(log_message)

# Import ES data
es = si.Importer("/home/robster970/repo/e-mini/sierrafiles/", "ESH18.dly_BarData.txt", "ES")
es_clean = es.get_data()
log_message = "ES clean data set ready for use."
logger.info(log_message)

# Import VIX data
vix = si.Importer("/home/robster970/repo/e-mini/sierrafiles/", "$VIX.dly_BarData.txt", "VIX")
vix_clean = vix.get_data()
log_message = "VIX clean data set ready for use."
logger.info(log_message)

# Tidy up VIX data to remove last two columns for volume and NumberOfTrades
vix_clean = vix_clean.iloc[:, 0:4]

# Create a single combined data frame to work from with NaN rows removed
combined = pd.concat([es_clean, vix_clean], axis=1)
combined = combined.dropna()
log_message = "Combined ES & VIX clean data set ready for use."
logger.info(log_message)

# Pass cleaned data frame to calculator for specific calculations from specific method for VIX.
vix_calc = sc.Calculator(combined, "VIX")
combined = vix_calc.calculate_values_vix(10)
log_message = "Additional columns with calculations returned from calculator for VIX"
logger.info(log_message)

# Pass cleaned data frame to calculator for specific calculations from specific method for ES.
es_calc = sc.Calculator(combined, "ES")
combined = es_calc.calculate_values_es(10)
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
print("-------------------------------------------------------------------------")
print(es_evaluated_data)
print("-------------------------------------------------------------------------")
print("Stop loss: " + str(es_stop_loss))
print("-------------------------------------------------------------------------")

# Experiments to turn to JSON object but currently missing the index which isn't too hot.
# Needs fixing.
# print(es_evaluated_data.iloc[0].to_json(orient='index'))
# print(es_evaluated_data.iloc[1].to_json(orient='index'))

# Run a backtest
sb.Backtest(combined).es_vix_long_test()

plt.show()
plt.figure(1)
plt.subplot(211)
combined['ES_Stop'].tail(20).plot(color='red')
plt.subplot(212)
combined['VIX_Ndt'].tail(20).plot(color='blue')
plt.subplot(212)
# plt.plot(combined.index, combined['ES_Stop'], 'bs', combined.index, combined['VIX_Pdf', 'g^'])
plt.show()
