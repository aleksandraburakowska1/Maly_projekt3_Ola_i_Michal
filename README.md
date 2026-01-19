{
  "nbformat": 4,
  "nbformat_minor": 0,
  "metadata": {
    "colab": {
      "provenance": []
    },
    "kernelspec": {
      "name": "python3",
      "display_name": "Python 3"
    },
    "language_info": {
      "name": "python"
    }
  },
  "cells": [
    {
      "cell_type": "markdown",
      "source": [
        "**Analiza danych PM2.5 w Polsce**\n",
        "\n",
        "Projekt dotyczy analizy stężenia pyłu PM2.5 na podstawie danych pomiarowych z różnych stacji w Polsce. W projekcie obliczane są średnie wartości, identyfikowane są dni z przekroczeniem normy oraz tworzone są wykresy porównawcze."
      ],
      "metadata": {
        "id": "GYTjUYwboeXN"
      }
    },
    {
      "cell_type": "markdown",
      "source": [
        "**Struktura projektu**"
      ],
      "metadata": {
        "id": "pjNt_BSEpCnP"
      }
    },
    {
      "cell_type": "markdown",
      "source": [
        "```text\n",
        "Maly_projekt3_Ola_i_Michal/\n",
        "|-- __pycache__/\n",
        "|-- tests/\n",
        "|-- Metadane oraz kody stacji i stanowisk pomiarowych.xlsx\n",
        "|-- PM25_all_years.csv        # główny zbiór danych\n",
        "|-- dokumentacja.txt\n",
        "|-- init.py\n",
        "|-- io_clean.py               # wczytywanie i czyszczenie danych\n",
        "|-- metrics.py                # obliczanie statystyk i norm\n",
        "|-- viz.py                    # generowanie wykresów\n",
        "|-- projekt_1_student.ipynb   # notatnik główny\n",
        "|-- requirements.txt\n",
        "\n"
      ],
      "metadata": {
        "id": "I7vVtdwrp2E_"
      }
    },
    {
      "cell_type": "markdown",
      "source": [
        "**Zadania**\n"
      ],
      "metadata": {
        "id": "UVELL5z3qMAI"
      }
    },
    {
      "cell_type": "markdown",
      "source": [
        "\n",
        "**Zadanie 1 – Wczytanie i czyszczenie danych**\n",
        "\n",
        "- import danych z plików CSV\n",
        "\n",
        "- usunięcie braków i błędnych rekordów\n",
        "\n",
        "- konwersja kolumny daty do typu datetime"
      ],
      "metadata": {
        "id": "DP5gP0v_qV66"
      }
    },
    {
      "cell_type": "markdown",
      "source": [
        "**Zadanie 2 – Obliczanie średnich**\n",
        "\n",
        "Obliczanie średnich ze wzorem:\n",
        "\n",
        "   $ \\overline{x} = \\frac{1}{n}\\sum_{i=1}^n x_i $\n",
        "\n",
        "- W kodzie liczone są średnie dobowe oraz miesięczne\n",
        "\n",
        "- rysowanie liniowych wykresów\n",
        "\n",
        "- porównania lat i lokalizacji zgodnie z treścią zadania\n"
      ],
      "metadata": {
        "id": "wFiID7_Oq6V0"
      }
    },
    {
      "cell_type": "markdown",
      "source": [
        "**Zadanie 3 – Wizualizacja**\n",
        "\n",
        "Wykonanie heatmap miesięcznych średnich dla miast"
      ],
      "metadata": {
        "id": "vwjJaMC_suKI"
      }
    },
    {
      "cell_type": "markdown",
      "source": [
        "**Zadanie 4 – Przekroczenia normy:**\n",
        "- zliczanie dni z przekroczeniem dopuszczalnej wartości i liczby przekroczeń dla wybranych stacji\n",
        "- wizualizacja na wykresie i interpretacja"
      ],
      "metadata": {
        "id": "HM_Y55zhtemo"
      }
    },
    {
      "cell_type": "markdown",
      "source": [
        "**Wymagania pakietów**\n",
        "\n",
        "Projekt wykorzystuje następujące biblioteki:\n",
        "\n",
        "- numpy  \n",
        "- pandas  \n",
        "- matplotlib  \n",
        "- seaborn  \n",
        "- requests  \n",
        "- pytest  \n",
        "\n",
        "Wymagana jest również nowa wersja Pythona >3.10\n",
        "\n",
        "Instalacja pakietów:\n",
        "```bash\n",
        "pip install -r requirements.txt"
      ],
      "metadata": {
        "id": "fQPZztKduXxc"
      }
    },
    {
      "cell_type": "markdown",
      "source": [
        "**Pliki:**\n",
        "\n",
        "Wymienione poniżej pliki są wczytywane przez plik projekt_1_student.ipynb, zawierają one funkcje potrzebne do realizacji zadań, dzięki takiemu rozwiązaniu kod jest uporządkowany i czytelny.\n",
        "- io_clean.py\n",
        "- metrics.py\n",
        " - viz.py\n"
      ],
      "metadata": {
        "id": "z2mMmapnviGM"
      }
    },
    {
      "cell_type": "markdown",
      "source": [
        "**Instalacja:**\n",
        "- sklonuj repozytorium:\n",
        "\n",
        "https://github.com/aleksandraburakowska1/Maly_projekt3_Ola_i_Michal.git\n",
        "\n",
        "- można zainstalować wirtualne środowisko\n",
        "- zainstaluj odpowiednie pakiety\n"
      ],
      "metadata": {
        "id": "EWF6o-BGxB0s"
      }
    },
    {
      "cell_type": "markdown",
      "source": [
        "**Uruchomienie testów:**\n",
        "\n",
        "PYTHONPATH=. pytest"
      ],
      "metadata": {
        "id": "Ru2Sr86-zFwX"
      }
    },
    {
      "cell_type": "markdown",
      "source": [
        "**Autorzy:**\n",
        "\n",
        "Aleksandra Burakowska, Michał Pszenicyn"
      ],
      "metadata": {
        "id": "VP4KIa4NzzBU"
      }
    }
  ]
}
