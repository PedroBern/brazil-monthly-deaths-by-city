from unittest import TestCase
import pandas as pd
import numpy as np

from brazil_monthly_deaths.exceptions import WrongInput
from brazil_monthly_deaths import (
    update_df,
    data_2015,
)

columns = ["city_id", "year", "month", "region", "state", "city", "deaths"]


class TestUpdateNewData(TestCase):
    def setUp(self):
        fake_data = [[82280746, 2015, 1, "North", "Acre", "Brasiléia", 10]]
        self.fake_df = pd.DataFrame(np.asarray(fake_data), columns=columns)

    def test_update_df_wrong_dtype(self):
        with self.assertRaises(WrongInput):
            updated_df = update_df(data_2015, self.fake_df)

    def test_update_df(self):
        self.fake_df["city_id"] = pd.to_numeric(self.fake_df["city_id"])
        self.fake_df["year"] = pd.to_numeric(self.fake_df["year"])
        self.fake_df["month"] = pd.to_numeric(self.fake_df["month"])
        self.fake_df["deaths"] = pd.to_numeric(self.fake_df["deaths"])
        updated_df = update_df(data_2015, self.fake_df)
        assert len(data_2015) == len(updated_df)
