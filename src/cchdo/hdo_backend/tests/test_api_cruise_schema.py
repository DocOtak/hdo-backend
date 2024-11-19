import json
import pytest
from jsonpointer import JsonPointer
from pydantic import ValidationError

from cchdo.hdo_backend.schemas import Cruise


def test_valid_cruise_document(cruise_json):
    Cruise.model_validate_json(json.dumps(cruise_json))


@pytest.mark.parametrize(
    "pointer,value",
    [
        ("/startDate", ""),
        ("/endDate", ""),
        ("/country", ""),
        ("/sites", {}),
        (
            "/collections/woce_lines",
            [
                "hi ",
            ],
        ),
        (
            "/collections/programs",
            [
                "hi ",
            ],
        ),
        (
            "/collections/oceans",
            [
                "hi ",
            ],
        ),
        (
            "/collections/groups",
            [
                "hi ",
            ],
        ),
        ("/cf_robots", ["bottle", "ctd", "summary"]),
    ],
)
def test_valid_cruise_document_set(cruise_json, pointer, value):
    p = JsonPointer(pointer)
    p.set(cruise_json, value)
    Cruise.model_validate_json(json.dumps(cruise_json))


@pytest.mark.parametrize(
    "pointer",
    [
        "/references",
        "/sites",
        "/license",
    ],
)
def test_valid_cruise_document_del(cruise_json, pointer):
    p = JsonPointer(pointer)
    subobj, part = p.to_last(cruise_json)
    del subobj[part]
    Cruise.model_validate_json(json.dumps(cruise_json))


@pytest.mark.parametrize(
    "pointer,message",
    [
        ("/collections", "collections"),
        ("/expocode", "expocode"),
        ("/ship", "ship"),
        ("/startDate", "startDate"),
        ("/endDate", "endDate"),
        ("/country", "country"),
        ("/participants", "participants"),
        ("/notes", "notes"),
        ("/geometry", "geometry"),
        ("/references/0/organization", "organization"),
        ("/references/0/type", "type"),
        ("/references/0/value", "value"),
        ("/geometry/track/coordinates/0/0", "too short"),
    ],
)
def test_invalid_cruise_document_del(cruise_json, pointer, message):
    p = JsonPointer(pointer)
    subobj, part = p.to_last(cruise_json)
    del subobj[part]
    with pytest.raises(ValidationError):
        Cruise.model_validate_json(json.dumps(cruise_json))


@pytest.mark.parametrize(
    "pointer,value,message",
    [
        ("/geometry/track/type", "Point", "not one of"),
        ("/geometry/track/coordinates/0/0", "blah", "not of type"),
        ("/geometry/track/coordinates/0", [0, 0, 0], "too long"),
        (
            "/geometry/track/coordinates/0",
            [
                0,
            ],
            "too short",
        ),
        ("/geometry/track/coordinates", [], "too short"),
        ("/geometry/track/coordinates", [[0, 0]], "too short"),
        # date things
        ("/startDate", "invalid", "not a date"),
        ("/startDate", "2015-01", "not a date"),
        ("/startDate", "2015", "not a date"),
        ("/endDate", "invalid", "not a date"),
        # disallow emptry strings in collections
        ("/collections/woce_lines", [""], "not match"),
        ("/collections/programs", [""], "not match"),
        ("/collections/oceans", [""], "not match"),
        ("/collections/groups", [""], "not match"),
        # disallow start with whitespace in collections
        ("/collections/woce_lines", [" hi"], "not match"),
        ("/collections/programs", [" hi"], "not match"),
        ("/collections/oceans", [" hi"], "not match"),
        ("/collections/groups", [" hi"], "not match"),
        # UK is not a country code, GB is
        ("/country", "UK", "not one of"),
        # references
        ("/references/0/organization", ["bad"], "not of type"),
        ("/references/0/type", ["bad"], "not of type"),
        ("/references/0/value", ["bad"], "not of type"),
        # some sites optional key tests
        ("/sites", [], "not of type"),
        ("/sites/microstructure.ucsd.edu", [], "not of type"),
        ("/sites/example.com", {}, "properties are not allowed"),
        # some license optional key tests
        ("/license/license", "Not Allowed", "not one of"),
        ("/license/name", "", "too short"),
        ("/license/email", "", "too short"),
        ("/license/institution", "", "too short"),
        ("/cf_robots", ["bottle", "random"], "not one of"),
    ],
)
def test_invalid_cruise_document_set(cruise_json, pointer, value, message):
    p = JsonPointer(pointer)
    p.set(cruise_json, value)
    with pytest.raises(ValidationError):
        Cruise.model_validate_json(json.dumps(cruise_json))
