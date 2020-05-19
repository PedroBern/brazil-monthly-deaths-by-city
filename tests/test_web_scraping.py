import pytest

from brazil_monthly_deaths import brazil_deaths
from brazil_monthly_deaths.exceptions import WrongInput


def test_raise_invalid_year():
    pytest.raises(WrongInput, brazil_deaths, years=[2000])


def test_raise_invalid_month():
    pytest.raises(WrongInput, brazil_deaths, months=[13])


def test_raise_invalid_state():
    pytest.raises(WrongInput, brazil_deaths, states=["invalid"])


def test_raise_invalid_region():
    pytest.raises(WrongInput, brazil_deaths, regions=["invalid"])
