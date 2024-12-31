# Take from upstox api docs, link can be found in source.md

# The keys might change because of change in financial year.
instrument_keys = {
    "Reliance":"NSE_EQ|INE002A01018",
    "TCS":"NSE_EQ|INE467B01029",
    "HDFC BANK":"NSE_EQ|INE040A01034",
    "ICICI BANK":"NSE_EQ|INE090A01021",
    "BHARTI AIRTEL":"NSE_EQ|INE397D01024"
}

# Initial Balance
BALANCE = 100_000

# Rules for Risk Management
MAX_NUMBER_OF_TRADES_PER_DAY = 4
PERCENT_MAX_LOSS_PER_DAY = 2 # percentage of BALANCE

# in side of trend full quantity else half quantity