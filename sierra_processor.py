import sierra_importer as si
import logger
import pandas as pd
import matplotlib.pyplot as plt


# Set up logger
processor_logger = logger.Logging()
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

print(combined.tail())
print(combined.describe())

combined['ES_Last'].tail(100).plot(color='red')
plt.show()
combined['VIX_Last'].tail(100).plot(color='green')
plt.show()
combined['ES_Vol'].hist(bins=50, color='purple')
plt.show()
