import pandas as pd
import numpy as np
from brazil_monthly_deaths import (
    update_df,
    data_2015,
)

columns = ["city_id", "year", "month", "region", "state", "city", "deaths"]

# create fake data
fake_data = [[82280746, 2015, 1, "North", "Acre", "Brasiléia", 10]]
fake_df = pd.DataFrame(np.asarray(fake_data), columns=columns)

# make sure the data has the correct dtype
fake_df["city_id"] = pd.to_numeric(fake_df["city_id"])
fake_df["year"] = pd.to_numeric(fake_df["year"])
fake_df["month"] = pd.to_numeric(fake_df["month"])
fake_df["deaths"] = pd.to_numeric(fake_df["deaths"])

# update the old data
updated_df = update_df(data_2015, fake_df)


def test_update_df():
    assert len(data_2015) == len(updated_df)
