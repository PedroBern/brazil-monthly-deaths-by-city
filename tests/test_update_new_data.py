import pandas as pd
from brazil_monthly_deaths import update_df

df1 = pd.DataFrame(
    {
        "A": ["A0", "A1", "A2", "A3"],
        "B": ["B0", "B1", "B2", "B3"],
        "C": ["C0", "C1", "C2", "C3"],
    }
)
df2 = pd.DataFrame({"A": ["A0", "A1"], "B": ["B0", "B4"], "C": ["C0", "C1"]})

duplicates = ["A", "B"]

df3 = update_df(df1, df2, duplicates)

df_correct = pd.DataFrame(
    {
        "A": ["A1", "A2", "A3", "A0", "A1"],
        "B": ["B1", "B2", "B3", "B0", "B4"],
        "C": ["C1", "C2", "C3", "C0", "C1"],
    }
)


def test_update_df():
    assert df3.equals(df_correct)
