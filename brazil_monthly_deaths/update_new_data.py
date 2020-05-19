import pandas as pd


duplicates = ["city_id", "year", "month", "region", "state", "city"]


def update_df(old_df, new_df, duplicates=duplicates):
    """
    old_df can be one of the provided by this package
    new_df is the fresh result from web scraping with brazil_deaths()

    example:
        new_df = brazil_deaths(years=[2020], months=[5], return_df=True)
    """
    df = pd.concat([old_df, new_df]).drop_duplicates(
        duplicates, keep="last", ignore_index=True,
    )
    return df
