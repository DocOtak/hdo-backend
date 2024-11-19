import json
from importlib.resources import files

import pytest

from . import data



@pytest.fixture(scope="function")
def cruise_json():
    return json.loads(files(data).joinpath("cruise.json").read_text())


@pytest.fixture(scope="function")
def file_json():
    return json.loads(files(data).joinpath("file.json").read_text())