"""
Web Scraping of Brazil Deaths
"""
import hashlib
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
import numpy as np
import pandas as pd

from .exceptions import WrongInput

# From where the data comes
url = "https://transparencia.registrocivil.org.br/registros"

# State names of Brazil
north_states = ["Acre", "Amazonas", "Amapá", "Pará", "Rondônia", "Roraima", "Tocantins"]
south_states = ["Paraná", "Rio Grande do Sul", "Santa Catarina"]
southeast_states = ["Espírito Santo", "Minas Gerais", "Rio de Janeiro", "São Paulo"]
center_west_states = ["Distrito Federal", "Goiás", "Mato Grosso do Sul", "Mato Grosso"]
northeast_states = [
    "Alagoas",
    "Bahia",
    "Ceará",
    "Maranhão",
    "Paraíba",
    "Pernambuco",
    "Piauí",
    "Rio Grande do Norte",
    "Sergipe",
]

# Regions of Brazil (defined above)
_regions = {
    "North": north_states,
    "Northeast": northeast_states,
    "South": south_states,
    "Southeast": southeast_states,
    "Center_West": center_west_states,
}

# Region names
_regions_names = ["North", "Northeast", "South", "Southeast", "Center_West"]

# dataframe
df_states = pd.DataFrame(dict([(k, pd.Series(v)) for k, v in _regions.items()]))
df_states = pd.melt(
    df_states, value_vars=_regions_names, var_name="region", value_name="state"
)
df_states = df_states.dropna()
df_states = df_states.reset_index(drop=True)

# flatten states
_states = [j for i in [i for i in _regions.values()] for j in i]

# Months in portuguese
_months = [
    "Janeiro",
    "Fevereiro",
    "Março",
    "Abril",
    "Maio",
    "Junho",
    "Julho",
    "Agosto",
    "Setembro",
    "Outubro",
    "Novembro",
    "Dezembro",
]

# Years with data available
_years = [2020, 2019, 2018, 2017, 2016, 2015]

# paths on the webpage
# if the webpage is updtaed and change these,
# the scrip will no longer work and need to be
# updated accordingly
year_path = '//fieldset[@id="datePickrGroup"]/div'
month_path = '//fieldset[@id="__BVID__39"]/div'
state_path = '//div[@id="__BVID__47"]/div'
search_path = '//button[normalize-space()="Pesquisar"]'
city_name_row_path = "//tbody/tr/td[@aria-colindex=1]"
city_deaths_row_path = "//tbody/tr/td[@aria-colindex=2]"
table_id = "__BVID__170"
next_page_path = '//li/a/span[text()="›"]/ancestor::li'
empty_table_path = '//tr[@class="b-table-empty-row"]'

# pandas df headers
header = ["city_id", "year", "month", "region", "state", "city", "deaths"]


def open_page():
    """
    open the webpage
    """
    browser.get(url)
    assert "Portal da Transparência" in browser.title


def select_deaths():
    """
    select the deaths radio input
    """
    browser.find_element_by_xpath(
        '//input[@id="__BVID__30__BV_radio_3_opt_"]/parent::div'
    ).click()


def select_field(path, data):
    """
    select the target data in the form
    """
    browser.find_element_by_xpath(path).click()
    browser.find_element_by_xpath(
        path + '/div/div/ul/li/span/span[text()="' + str(data) + '"]/ancestor::li'
    ).click()


def press_search():
    """
    press the search button
    """
    wait.until(EC.element_to_be_clickable((By.XPATH, search_path)))
    button = browser.find_element_by_xpath(search_path)
    actions = ActionChains(browser)
    actions.move_to_element(button).click(button).perform()


def select_fields(year, month, state):
    """
    select the year, month and state, then press the search
    """
    month = _months[month - 1]  # convert month from number to portuguese word
    select_field(year_path, year)
    select_field(month_path, month)
    select_field(state_path, state)
    press_search()


def get_table_data():
    """
    return city names and deaths number
    if the table is empty, return False
    """
    wait.until(
        EC.presence_of_element_located(
            (By.XPATH, empty_table_path + "|" + city_name_row_path)
        )
        # or EC.presence_of_element_located((By.XPATH, city_name_row_path))
    )
    empty_table = len(browser.find_elements_by_xpath(empty_table_path)) != 0

    if not empty_table:
        cities = [
            item.text for item in browser.find_elements_by_xpath(city_name_row_path)
        ]
        deaths = [
            item.text for item in browser.find_elements_by_xpath(city_deaths_row_path)
        ]
        return {"cities": cities, "deaths": deaths}
    else:
        return False


def next_page():
    """
    if there is the next page button, press it
    """
    try:
        browser.find_element_by_xpath(next_page_path).click()
        return True
    except:
        return False


def save_data(data, year, filename="data", *args, **kwargs):
    """
    save the data as csv
    """
    filename += "_" + year + ".csv"
    data.to_csv(filename, index=False, header=header, *args, **kwargs)


def make_city_id(state, city):
    s = state + " " + city
    hash = int(hashlib.sha256(s.encode("utf-8")).hexdigest(), 16) % 10 ** 8
    return hash


def brazil_deaths(
    years=_years,
    months=range(1, 13, 1),
    regions=_regions_names,
    states=_states,
    filename="data",
    return_df=True,
    save_csv=True,
    verbose=True,
    *args,
    **kwargs
):
    """
        save the tidy data as csv for each year and/or return a pandas df
    """

    # check the inputs
    if not set(years).issubset(set(_years)):
        raise WrongInput("Year must be between 2015 and 2020")
    if not set(months).issubset(set(range(1, 13, 1))):
        raise WrongInput("Months must be between 1 and 12")
    if not set(states).issubset(set(_states)):
        raise WrongInput("Invalid states")
    if not set(regions).issubset(set(_regions_names)):
        raise WrongInput("Invalid regions")

    # order the months
    months = sorted(months)

    # filter rows based on input and group by regions
    _df_states = df_states.query("region in @regions")
    _df_states = _df_states.query("state in @states")
    _df_states = _df_states.groupby("region")

    # do the web scraping
    global browser, wait
    browser = webdriver.Chrome()
    wait = WebDriverWait(browser, 60)

    open_page()
    select_deaths()
    if return_df:
        combined_df = pd.DataFrame(columns=header)
    for year in years:
        if verbose:
            print("year:", year)
        year_data = []
        for month in months:
            if verbose:
                print("month:", month)
            for region, df_group in _df_states:
                if verbose:
                    print("region:", region)
                for index, row in df_group.iterrows():
                    state = row["state"]
                    if verbose:
                        print("state:", state)
                    select_fields(year, month, state)
                    next_p = True
                    page = 1
                    state_cities = []
                    state_deaths = []
                    while next_p:
                        if verbose:
                            print("page:", page)
                        d = get_table_data()
                        if d is not False:
                            state_cities += d["cities"]
                            state_deaths += d["deaths"]
                        next_p = next_page()
                        page += 1
                    for c, city in enumerate(state_cities):
                        city_id = make_city_id(state, city)
                        year_data.append(
                            [
                                city_id,
                                year,
                                month,
                                region,
                                state,
                                city,
                                state_deaths[c],
                            ]
                        )
        if len(year_data) > 0:
            df = pd.DataFrame(np.asarray(year_data), columns=header)
            if save_csv:
                save_data(df, str(year), filename=filename, *args, **kwargs)
            if return_df:
                combined_df = combined_df.append(df)
    browser.quit()
    if return_df:
        if len(combined_df) > 0:
            combined_df["city_id"] = pd.to_numeric(combined_df["city_id"])
            combined_df["year"] = pd.to_numeric(combined_df["year"])
            combined_df["month"] = pd.to_numeric(combined_df["month"])
            combined_df["deaths"] = pd.to_numeric(combined_df["deaths"])
            return combined_df
        else:
            return None
