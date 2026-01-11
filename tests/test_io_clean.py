import pytest
import pandas as pd
from io_clean import use_station_header, build_kod2miasto, build_old2new

def test_use_station_header():
    df = pd.DataFrame([
        ["Coś", "Inne", "Dalsze"],
        ["Kod stacji", "ST1", "ST2"],
        ["2023-01-01 00:00:00", 10, 20]
    ])
    df_out = use_station_header(df)
    
    assert list(df_out.columns) == ["Data", "ST1", "ST2"]
    assert len(df_out) == 2
    assert df_out.iloc[1]["ST1"] == 10

def test_build_kod2miasto():
    dfmeta = pd.DataFrame([
        ["Kod stacji", "Miejscowość", "Inne"],
        ["ST1", "Warszawa", "x"],
        ["ST2", "Kraków", "y"]
    ])
    res = build_kod2miasto(dfmeta)
    assert res == {"ST1": "Warszawa", "ST2": "Kraków"}

def test_build_old2new():
    dfmeta = pd.DataFrame([
        ["Kod stacji", "Stary kod stacji"],
        ["NEW1", "OLD1"],
        ["NEW2", "OLD2, OLD2B"]
    ])
    res = build_old2new(dfmeta)
    assert res == {
        "OLD1": "NEW1",
        "OLD2": "NEW2",
        "OLD2B": "NEW2"
    }
