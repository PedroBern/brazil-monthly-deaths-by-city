from .dataframes import (
    data_2015,
    data_2016,
    data_2017,
    data_2018,
    data_2019,
    data_2020,
    data,
)
from .update_new_data import update_df
from .web_scraping import brazil_deaths

__all__ = [
    "brazil_deaths",
    "update_df",
    "data_2015",
    "data_2016",
    "data_2017",
    "data_2018",
    "data_2019",
    "data_2020",
    "data",
]

__version__ = "1.0.1"
