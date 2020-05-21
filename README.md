# Brazil Monthly Deaths by City

Web Scraping Package of Brazil Deaths.

[![Codecov Coverage](https://img.shields.io/codecov/c/github/pedrobern/brazil-monthly-deaths-by-city/master.svg?style=flat-square)](https://codecov.io/gh/pedrobern/brazil-monthly-deaths-by-city/)
[![Build Status](https://travis-ci.com/pedrobern/brazil-monthly-deaths-by-city.svg?branch=master)](https://travis-ci.com/pedrobern/brazil-monthly-deaths-by-city)
[![Pypi](https://img.shields.io/pypi/v/brazil-monthly-deaths.svg)](https://pypi.org/project/brazil-monthly-deaths/)
[![contributions welcome](https://img.shields.io/badge/contributions-welcome-brightgreen.svg?style=flat)](https://github.com/pedrobern/brazil-monthly-deaths-by-city/blob/master/CONTRIBUTING.md)

## Table of Content

- [Installation](#Installation)
- [Usage](#Usage)
- [Data example](#Data-example)
- [API](#API)
  - [Dataframes](#Dataframes)
  - [brazil_deaths](#brazil-deaths)
  - [update_df](#update-df)

<div id="Installation"></div>

## Installation

First install the package:

```bash
pip install brazil-monthly-deaths
```

Then install the chrome driver in order to use selenium, you can see more information in the [selenium documentation](https://selenium-python.readthedocs.io/installation.html#drivers) and the [chrome driver download page](https://sites.google.com/a/chromium.org/chromedriver/downloads).

<div id="Usage"></div>

## Usage

> Assuming you have installed the chrome driver

```python
from brazil_monthly_deaths import brazil_deaths, data, update_df

# data is the data from 2015 to 2020
print(data)

# Everyday there are new records,
# so you should get the most recent data.
# Depending on your internet connection
# it may take up to 6 minutes for each month
# if you run for all states. Consider selecting
# only the states you want to work on.
new_data = brazil_deaths(years=[2020], months=[5])

# update the lagging data provided by this package
current_data = update_df(data, new_data)
print(current_data)
```

<div id="Data-example"></div>

## Data example

| city_id  | year | month | region    | state          | city        | deaths |
|----------|------|-------|-----------|----------------|-------------|--------|
| 3516805  | 2020 | 1     | Southeast | Rio de Janeiro | Tracunhaém  | 8      |
| 21835289 | 2020 | 1     | Southeast | Rio de Janeiro | Trindade    | 13     |
| 10791950 | 2020 | 1     | Southeast | Rio de Janeiro | Triunfo     | 16     |
| 81875827 | 2020 | 1     | Southeast | Rio de Janeiro | Tupanatinga | 18     |
| 99521011 | 2020 | 1     | Southeast | Rio de Janeiro | Tuparetama  | 4      |


---

<div id="API"></div>

## API

<div id="Dataframes"></div>

### Dataframes

This package exports some [pandas](https://github.com/pandas-dev/pandas) dataframe with the following columns:

- city_id : unique integer from state and city,
- year : from 2015 to 2020,
- month : from 1 to 12,
- region : [North, Northeast, South, Southeast, Center_West],
- state : one of the 27 states of Brazil, including country capital,
- city : city name
- deaths : number os deaths

```python
from brazil_monthly_deaths import (
  data, # full data
  data_2015,
  data_2016,
  data_2017,
  data_2018,
  data_2019,
  data_2020 # always out of date, you need to update it
)
```

<div id="brazil-deaths"></div>

### brazil_deaths

You can use this function to scrap new data directly from the [Civil Registry Offices website](https://transparencia.registrocivil.org.br/registros). Just make sure you have installed the chrome driver, as pointed above.

Oficial note about the legal deadlines:

> The family has up to 24 hours after the death to register the death in the Registry, which, in turn, has up to five days to perform the death registration, and then up to eight days to send the act done to the National Information Center of the Civil Registry ( CRC Nacional), which updates this platform.

It means: **The last 13 days are always changing.**

```python
from brazil_monthly_deaths import brazil_deaths
```

Since it will access an external website, it will depend on your internet connection and world location. Consider selecting only the `states` you want to work on. For each month, for all states it may take up to 6 min to run for a single year.

```python
df = brazil_deaths(
    years=[2015, 2016, 2017, 2018, 2019, 2020],
    months=range(1, 13, 1),
    regions=_regions_names,
    states=_states,
    filename="data",
    return_df=True,
    save_csv=True,
    verbose=True,
    *args,
    **kwargs
)  
```

The `_regions_names` is:

```python
["North", "Northeast", "South", "Southeast", "Center_West"]
```

The `_states` is:

```python
[
  "Acre", "Amazonas", "Amapá", "Pará", 
  "Rondônia", "Roraima", "Tocantins", "Paraná",
  "Rio Grande do Sul", "Santa Catarina", "Espírito Santo",
  "Minas Gerais", "Rio de Janeiro", "São Paulo",
  "Distrito Federal", "Goiás", "Mato Grosso do Sul",
  "Mato Grosso", "Alagoas", "Bahia", "Ceará",
  "Maranhão", "Paraíba", "Pernambuco",
  "Piauí", "Rio Grande do Norte", "Sergipe"
]
```

The `*args` and `**kwargs` are passed down to `df.to_csv(..., *args, **kwargs)`

<div id="update-df"></div>

### update_df

Use this function after you have scraped recent data from the Civil Registry Offices website to update the data provided in this package.

```python
from brazil_monthly_deaths import brazil_deaths, data, update_df

new_data = brazil_deaths(years=[2020], months=[5])
current_data = update_df(data, new_data)
```

It basically put the new data below the old data in the dataframe, then remove the duplicates (excluding deaths) keeping the most recent entries.
