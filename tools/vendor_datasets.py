from __future__ import annotations

import sys
from functools import cached_property, partial
from pathlib import Path
from typing import Any, Literal, cast
from urllib.request import urlopen

if sys.version_info >= (3, 10):
    from typing import TypeAlias
else:
    from typing_extensions import TypeAlias

import polars as pl

# This is the tag in http://github.com/vega/vega-datasets from
# which the datasets in this repository are sourced.
SOURCE_TAG = "v1.29.0"  # 5 years ago
CURRENT_TAG = "v2.9.0"
USE_TAG = CURRENT_TAG

BASE_URL = f"https://cdn.jsdelivr.net/npm/vega-datasets@{USE_TAG}/data/"

ExtSupported: TypeAlias = Literal[".csv", ".json", ".tsv"]


class Dataset:
    def __init__(self, name: str, /) -> None:
        self.name: str = name
        js_name = name.replace("_", "-")
        file_name = DATASETS_JSON[js_name]["filename"]
        suffix = Path(file_name).suffix
        self.extension: ExtSupported
        if suffix in {".csv", ".json", ".tsv"}:
            self.extension = cast(ExtSupported, suffix)
        else:
            raise NotImplementedError(suffix, file_name)

        self.url: str = f"{BASE_URL}{file_name}"

    def __call__(self, **kwds: Any) -> pl.DataFrame:
        with urlopen(self.url) as f:
            content = ext_fn(self.extension, **kwds)(f)
        return content

    def __repr__(self) -> str:
        return (
            f"{type(self).__name__}(\n  "
            f"name={self.name!r},\n  "
            f"url={self.url!r}\n"
            ")"
        )


def ext_fn(ext: ExtSupported, /):
    """Very basic mapping to `polars` eager functions."""
    if ext == ".csv":
        return pl.read_csv
    elif ext == ".json":
        return pl.read_json
    elif ext == ".tsv":
        return partial(pl.read_csv, separator="\t")
    else:
        raise


DATASET_NAMES_USED = [
    "airports",
    "anscombe",
    "barley",
    "cars",
    "co2_concentration",
    "countries",
    "disasters",
    "driving",
    "earthquakes",
    "flights_2k",
    "flights_5k",
    "flights_airport",
    "gapminder_health_income",
    "github",
    "income",
    "iowa_electricity",
    "iris",
    "jobs",
    "londonBoroughs",
    "londonCentroids",
    "londonTubeLines",
    "monarchs",
    "movies",
    "normal_2d",
    "ohlc",
    "population",
    "population_engineers_hurricanes",
    "seattle_weather",
    "sp500",
    "stocks",
    "unemployment",
    "unemployment_across_industries",
    "us_10m",
    "us_employment",
    "us_state_capitals",
    "us_unemployment",
    "wheat",
    "windvectors",
    "world_110m",
    "zipcodes",
]

DATASETS_JSON = {
    # "7zip": {"filename": "7zip.png", "format": "png"},
    "airports": {"filename": "airports.csv", "format": "csv"},
    "annual-precip": {"filename": "annual-precip.json", "format": "json"},
    "anscombe": {"filename": "anscombe.json", "format": "json"},
    "barley": {"filename": "barley.json", "format": "json"},
    "birdstrikes": {"filename": "birdstrikes.json", "format": "json"},
    "budget": {"filename": "budget.json", "format": "json"},
    "budgets": {"filename": "budgets.json", "format": "json"},
    "burtin": {"filename": "burtin.json", "format": "json"},
    "cars": {"filename": "cars.json", "format": "json"},
    "climate": {"filename": "climate.json", "format": "json"},
    "co2-concentration": {"filename": "co2-concentration.csv", "format": "csv"},
    "countries": {"filename": "countries.json", "format": "json"},
    "crimea": {"filename": "crimea.json", "format": "json"},
    "disasters": {"filename": "disasters.csv", "format": "csv"},
    "driving": {"filename": "driving.json", "format": "json"},
    "earthquakes": {"filename": "earthquakes.json", "format": "json"},
    # "ffox": {"filename": "ffox.png", "format": "png"},
    "flare": {"filename": "flare.json", "format": "json"},
    "flare-dependencies": {"filename": "flare-dependencies.json", "format": "json"},
    "flights-10k": {"filename": "flights-10k.json", "format": "json"},
    "flights-200k": {"filename": "flights-200k.json", "format": "json"},
    "flights-20k": {"filename": "flights-20k.json", "format": "json"},
    "flights-2k": {"filename": "flights-2k.json", "format": "json"},
    "flights-3m": {"filename": "flights-3m.csv", "format": "csv"},
    "flights-5k": {"filename": "flights-5k.json", "format": "json"},
    "flights-airport": {"filename": "flights-airport.csv", "format": "csv"},
    "gapminder": {"filename": "gapminder.json", "format": "json"},
    "gapminder-health-income": {
        "filename": "gapminder-health-income.csv",
        "format": "csv",
    },
    # "gimp": {"filename": "gimp.png", "format": "png"},
    "github": {"filename": "github.csv", "format": "csv"},
    "graticule": {"filename": "graticule.json", "format": "json"},
    "income": {"filename": "income.json", "format": "json"},
    "iowa-electricity": {"filename": "iowa-electricity.csv", "format": "csv"},
    "iris": {"filename": "iris.json", "format": "json"},
    "jobs": {"filename": "jobs.json", "format": "json"},
    "la-riots": {"filename": "la-riots.csv", "format": "csv"},
    "londonBoroughs": {"filename": "londonBoroughs.json", "format": "json"},
    "londonCentroids": {"filename": "londonCentroids.json", "format": "json"},
    "londonTubeLines": {"filename": "londonTubeLines.json", "format": "json"},
    "lookup_groups": {"filename": "lookup_groups.csv", "format": "csv"},
    "lookup_people": {"filename": "lookup_people.csv", "format": "csv"},
    "miserables": {"filename": "miserables.json", "format": "json"},
    "monarchs": {"filename": "monarchs.json", "format": "json"},
    "movies": {"filename": "movies.json", "format": "json"},
    "normal-2d": {"filename": "normal-2d.json", "format": "json"},
    "obesity": {"filename": "obesity.json", "format": "json"},
    "ohlc": {"filename": "ohlc.json", "format": "json"},
    "points": {"filename": "points.json", "format": "json"},
    "population": {"filename": "population.json", "format": "json"},
    "population_engineers_hurricanes": {
        "filename": "population_engineers_hurricanes.csv",
        "format": "csv",
    },
    "seattle-temps": {"filename": "seattle-temps.csv", "format": "csv"},
    "seattle-weather": {"filename": "seattle-weather.csv", "format": "csv"},
    "sf-temps": {"filename": "sf-temps.csv", "format": "csv"},
    "sp500": {"filename": "sp500.csv", "format": "csv"},
    "stocks": {"filename": "stocks.csv", "format": "csv"},
    "udistrict": {"filename": "udistrict.json", "format": "json"},
    "unemployment": {"filename": "unemployment.tsv", "format": "tsv"},
    "unemployment-across-industries": {
        "filename": "unemployment-across-industries.json",
        "format": "json",
    },
    "uniform-2d": {"filename": "uniform-2d.json", "format": "json"},
    "us-10m": {"filename": "us-10m.json", "format": "json"},
    "us-employment": {"filename": "us-employment.csv", "format": "csv"},
    "us-state-capitals": {"filename": "us-state-capitals.json", "format": "json"},
    "volcano": {"filename": "volcano.json", "format": "json"},
    "weather": {"filename": "weather.json", "format": "json"},
    "weball26": {"filename": "weball26.json", "format": "json"},
    "wheat": {"filename": "wheat.json", "format": "json"},
    "windvectors": {"filename": "windvectors.csv", "format": "csv"},
    "world-110m": {"filename": "world-110m.json", "format": "json"},
    "zipcodes": {"filename": "zipcodes.csv", "format": "csv"},
}


class DataLoader:
    @cached_property
    def _dataset_names(self) -> list[str]:
        return sorted(DATASETS_JSON)

    @cached_property
    def _py_js_names(self) -> dict[str, str]:
        return {name.replace("-", "_"): name for name in self._dataset_names}

    def list_datasets(self) -> list[str]:
        return list(self._py_js_names)

    def __getattr__(self, name: str) -> Dataset:
        if name in self._py_js_names:
            return Dataset(self._py_js_names[name])
        else:
            msg = f"No dataset named '{name}'"
            raise AttributeError(msg)

    def __dir__(self) -> list[str]:
        return self.list_datasets()


data = DataLoader()
