import pandas as pd
import os

dir = os.path.dirname(os.path.realpath(__file__))

data_2015 = pd.read_csv(dir + "/data/data_2015.csv")
data_2016 = pd.read_csv(dir + "/data/data_2016.csv")
data_2017 = pd.read_csv(dir + "/data/data_2017.csv")
data_2018 = pd.read_csv(dir + "/data/data_2018.csv")
data_2019 = pd.read_csv(dir + "/data/data_2019.csv")
data_2020 = pd.read_csv(dir + "/data/data_2020.csv")

data = pd.concat(
    [data_2015, data_2016, data_2017, data_2018, data_2019, data_2020],
    ignore_index=True,
)
