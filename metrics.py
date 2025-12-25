#plik obsługujący: liczenie średnich i wskazywanie dni z przekroczeniem normy
import pandas as pd
from datetime import time
def ensure_datetime(df: pd.DataFrame) -> pd.DataFrame:
    """
    Konwertuje kolumnę z datą na datetime64 w znanym formacie '%Y-%m-%d %H:%M:%S'.
    Działa zarówno dla zwykłych kolumn, jak i MultiIndex.
    """
    df = df.copy()

    # znajdź kolumnę z datą
    date_col = None
    if isinstance(df.columns, pd.MultiIndex):
        for c in df.columns:
            if any(str(x).strip().lower() in ("data", "date", "czas") for x in (c if isinstance(c, tuple) else [c])):
                date_col = c
                break
    else:
        for c in df.columns:
            if str(c).strip().lower() in ("data", "date", "czas"):
                date_col = c
                break

    if date_col is None:
        raise ValueError("Nie znaleziono kolumny z datą.")

    # szybka konwersja z określonym formatem
    df[date_col] = pd.to_datetime(df[date_col], format="%Y-%m-%d %H:%M:%S", errors="coerce")

    n_na = df[date_col].isna().sum()
    print(f"Kolumna {date_col} przekonwertowana na datetime (błędne wartości: {n_na})")

    return df
def shift_midnight_to_prev_day(df: pd.DataFrame) -> pd.DataFrame:
    out = ensure_datetime(df)
    # znajdź kolumnę daty ponownie
    date_col = next(c for c in out.columns if ("data" in str(c).lower() or "date" in str(c).lower() or "czas" in str(c).lower()))
    m = out[date_col].dt.time == time(0, 0, 0)

    out.loc[m, date_col] = out.loc[m, date_col] - pd.Timedelta(seconds=1)
    #print(out.loc[m, date_col])  #tu faktycznie zobaczyłam przesunięcie daty
    #print(f"Przesunięto {int(m.sum())} wierszy z 00:00:00 na poprzedni dzień.")
    return out 

import pandas as pd

def to_long_pm25(df: pd.DataFrame) -> pd.DataFrame:
    """
    Zamienia tabelę szeroką (kolumny = stacje) na format long:
    Data | Rok | Kod_stacji | PM25
    """
    station_cols = [c for c in df.columns if c not in ["Data", "Rok"]]

    df_long = df.melt(
        id_vars=["Data", "Rok"],
        value_vars=station_cols,
        var_name="Kod_stacji",
        value_name="PM25"
    )

    return df_long
def add_city_and_month(
    df_long: pd.DataFrame,
    kod2miasto: dict
) -> pd.DataFrame:
    """
    Dodaje kolumny:
    - Miasto (na podstawie Kod_stacji)
    - Miesiac (z kolumny Data)
    Usuwa wiersze bez przypisanego miasta.
    """
    df = df_long.copy()

    # mapowanie kod -> miasto
    df["Miasto"] = df["Kod_stacji"].map(kod2miasto)

    # usunięcie stacji bez miasta
    df = df.dropna(subset=["Miasto"])

    # numer miesiąca
    df["Miesiac"] = df["Data"].dt.month

    return df
def monthly_station_mean(df: pd.DataFrame) -> pd.DataFrame:
    """
    Średnia miesięczna PM25 dla każdej stacji.
    """
    return (
        df
        .groupby(
            ["Rok", "Miasto", "Kod_stacji", "Miesiac"],
            as_index=False
        )["PM25"]
        .mean()
    )
def monthly_city_mean(df_station_month: pd.DataFrame) -> pd.DataFrame:
    """
    Średnia miesięczna PM25 dla miasta
    (uśrednienie po stacjach).
    """
    return (
        df_station_month
        .groupby(
            ["Rok", "Miasto", "Miesiac"],
            as_index=False
        )["PM25"]
        .mean()
    )
#tu daję też funkcje potrzebne do fragmentu zadania 4: liczenie dziennych średnich, dni z przekroczeniem, zliczanie dni, wybór top/bottom.
def daily_station_mean(df_long: pd.DataFrame) -> pd.DataFrame:
    """
    Liczy dzienne średnie PM2.5 dla każdej stacji i roku.
    Wymaga kolumn: Data (datetime), Rok, Kod_stacji, PM25
    Zwraca: Kod_stacji, Rok, Data (date), PM25 (średnia dzienna)
    """
    df = df_long.copy()
    df["Data"] = pd.to_datetime(df["Data"])
    df["Data"] = df["Data"].dt.date

    daily = (
        df.groupby(["Kod_stacji", "Rok", "Data"], as_index=False)["PM25"]
        .mean()
    )
    return daily


def exceedance_days_per_year(
    df_daily: pd.DataFrame,
    threshold: float = 15.0
) -> pd.DataFrame:
    """
    Zlicza liczbę dni w roku ze średnią dzienną > threshold dla każdej stacji.
    Zwraca: Kod_stacji, Rok, przekracza (liczba dni)
    """
    d = df_daily.copy()
    d["przekracza"] = (d["PM25"] > threshold).astype(int)

    counts = (
        d.groupby(["Kod_stacji", "Rok"], as_index=False)["przekracza"]
        .sum()
    )
    return counts


def select_top_bottom_stations(
    counts: pd.DataFrame,
    year: int,
    k: int = 3
) -> pd.Index:
    """
    Wybiera k stacji z największą i k z najmniejszą liczbą dni przekroczeń w danym roku.
    Zwraca listę kodów stacji (unikalne).
    """
    one_year = counts[counts["Rok"] == year]
    topk = one_year.nlargest(k, "przekracza")
    bottomk = one_year.nsmallest(k, "przekracza")
    selected = pd.concat([topk, bottomk])["Kod_stacji"].unique()
    return selected
