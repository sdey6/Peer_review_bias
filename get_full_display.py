import pandas as pd


def full_display():
    pd.options.display.width = None
    pd.options.display.max_columns = None
    pd.set_option('display.max_rows', 2000)
    pd.set_option('display.max_columns', 2000)


full_display()
