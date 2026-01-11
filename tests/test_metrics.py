import pytest
import pandas as pd
import numpy as np
from datetime import date, time
from metrics import (
    ensure_datetime, 
    shift_midnight_to_prev_day, 
    add_city_and_month,
    daily_station_mean,
    exceedance_days_per_year,
    select_top_bottom_stations
)

def test_ensure_datetime():
    df = pd.DataFrame({"Data": ["2023-01-01 12:00:00", "2023-01-02 00:00:00"]})
    df_out = ensure_datetime(df)
    assert pd.api.types.is_datetime64_any_dtype(df_out["Data"])
    assert df_out["Data"].iloc[0] == pd.Timestamp("2023-01-01 12:00:00")

def test_ensure_datetime_invalid():
    df = pd.DataFrame({"WrongColumn": ["2023-01-01"]})
    with pytest.raises(ValueError, match="Nie znaleziono kolumny z datą"):
        ensure_datetime(df)

def test_shift_midnight_to_prev_day():
    df = pd.DataFrame({"Data": ["2023-01-02 00:00:00", "2023-01-02 01:00:00"]})
    df_out = shift_midnight_to_prev_day(df)
    assert df_out["Data"].iloc[0] == pd.Timestamp("2023-01-01 23:59:59")
    assert df_out["Data"].iloc[1] == pd.Timestamp("2023-01-02 01:00:00")

def test_add_city_and_month():
    df = pd.DataFrame({
        "Kod_stacji": ["ST1", "ST2", "ST3"],
        "Data": pd.to_datetime(["2023-01-01", "2023-02-01", "2023-03-01"])
    })
    kod2miasto = {"ST1": "Warszawa", "ST2": "Kraków"}
    df_out = add_city_and_month(df, kod2miasto)
    
    assert len(df_out) == 2
    assert "Miasto" in df_out.columns
    assert "Miesiac" in df_out.columns
    assert df_out[df_out["Kod_stacji"] == "ST1"]["Miasto"].iloc[0] == "Warszawa"
    assert df_out[df_out["Kod_stacji"] == "ST1"]["Miesiac"].iloc[0] == 1
    assert df_out[df_out["Kod_stacji"] == "ST2"]["Miesiac"].iloc[0] == 2

def test_daily_station_mean():
    df = pd.DataFrame({
        "Kod_stacji": ["ST1", "ST1", "ST1"],
        "Rok": [2023, 2023, 2023],
        "Data": pd.to_datetime(["2023-01-01 10:00:00", "2023-01-01 14:00:00", "2023-01-02 10:00:00"]),
        "PM25": [10.0, 20.0, 30.0]
    })
    df_out = daily_station_mean(df)
    
    jan1 = df_out[(df_out["Kod_stacji"] == "ST1") & (df_out["Data"] == date(2023, 1, 1))]
    assert jan1["PM25"].iloc[0] == 15.0
    
    jan2 = df_out[(df_out["Kod_stacji"] == "ST1") & (df_out["Data"] == date(2023, 1, 2))]
    assert jan2["PM25"].iloc[0] == 30.0

def test_exceedance_days_per_year():
    df_daily = pd.DataFrame({
        "Kod_stacji": ["ST1", "ST1", "ST1"],
        "Rok": [2023, 2023, 2023],
        "Data": [date(2023, 1, 1), date(2023, 1, 2), date(2023, 1, 3)],
        "PM25": [10.0, 20.0, 30.0]
    })
    df_out = exceedance_days_per_year(df_daily, threshold=15.0)
    
    res = df_out[(df_out["Kod_stacji"] == "ST1") & (df_out["Rok"] == 2023)]
    assert res["przekracza"].iloc[0] == 2

def test_select_top_bottom_stations():
    counts = pd.DataFrame({
        "Kod_stacji": ["ST1", "ST2", "ST3", "ST4", "ST5"],
        "Rok": [2023]*5,
        "przekracza": [10, 2, 8, 1, 5]
    })
    selected = select_top_bottom_stations(counts, year=2023, k=1)
    assert set(selected) == {"ST1", "ST4"}
