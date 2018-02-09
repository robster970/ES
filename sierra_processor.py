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

# Pass cleaned data frame to calculator for specific calculations from specific methods.
es_calc = sc.Calculator(combined, "VIX")
combined = es_calc.calculate_values_vix(10)
log_message = "Additional columns with calculations returned from calculator"
processor_logger.parser(module, log_message)

# Make trading entry decision foe es_vix_long strategy
es_decision = st.Trading(combined)
log_message = es_decision.es_vix_long("entry")
processor_logger.parser(module, log_message)

# Make trading entry decision foe es_vix_long strategy
es_decision = st.Trading(combined)
log_message = es_decision.es_vix_long("exit")
processor_logger.parser(module, log_message)


combined['VIX_Ndt'].tail(20).plot(color='red')
plt.show()
combined['VIX_Pdf'].tail(20).plot(color='blue')
plt.show()
