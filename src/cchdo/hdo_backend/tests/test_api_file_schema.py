import json

import pytest
from jsonpointer import JsonPointer
from pydantic import ValidationError

from cchdo.hdo_backend.schemas import File


def test_valid_file_document(file_json):
    File.model_validate_json(json.dumps(file_json))


@pytest.mark.parametrize(
    "pointer,value",
    [
        ("/submissions/0/date", "2012-03-22T00:00:00Z"),
        ("/events", []),
        ("/other_roles", []),
    ],
)
def test_valid_file_document_set(file_json, pointer, value):
    p = JsonPointer(pointer)
    p.set(file_json, value)
    File.model_validate_json(json.dumps(file_json))


@pytest.mark.parametrize(
    "pointer",
    [
        "/file",
        "/description",
        "/references",
        "/projects",
        "/projects/katsumata_clean_data",
    ],
)
def test_valid_file_document_del(file_json, pointer):
    p = JsonPointer(pointer)
    subobj, part = p.to_last(file_json)
    del subobj[part]
    File.model_validate_json(json.dumps(file_json))


@pytest.mark.parametrize(
    "pointer,message",
    [
        ("/file_hash", "file_hash"),
        ("/file_name", "file_name"),
        ("/file_size", "file_size"),
        ("/file_type", "file_type"),
        ("/file_sources", "file_sources"),
        ("/role", "role"),
        ("/events", "events"),
        ("/other_roles", "other_roles"),
        ("/data_container", "data_container"),
        ("/data_type", "data_type"),
        ("/data_format", "data_format"),
        ("/container_contents", "container_contents"),
        ("/submissions", "submissions"),
        ("/submissions/0/date", "date"),
        # references subobject
        ("/references/0/organization", "organization"),
        ("/references/0/type", "type"),
        ("/references/0/value", "value"),
        # events subobject
        ("/events/0/date", "date"),
        ("/events/0/type", "type"),
        ("/events/0/name", "name"),
        ("/events/0/notes", "notes"),
    ],
)
def test_invalid_file_document_del(file_json, pointer, message):
    p = JsonPointer(pointer)
    subobj, part = p.to_last(file_json)
    del subobj[part]
    with pytest.raises(ValidationError):
        File.model_validate_json(json.dumps(file_json))


@pytest.mark.parametrize(
    "pointer,value,message",
    [
        (
            "/example",
            {},
            "Additional properties are not allowed ('example' was unexpected)",
        ),
        ("/file_name", "", "'' is too short"),
        ("/submissions/0/date", "nat", "invalid submission date"),
        ("/references/0/organization", ["bad"], "['bad'] is not of type 'string'"),
        (
            "/references/0/type",
            ["bad"],
            "['bad'] is not of type 'string'\n['bad'] is not one of ['doi', 'ark', 'alias', 'award', 'accession', 'citation', 'link', 'related', 'float']",
        ),
        ("/references/0/value", ["bad"], "['bad'] is not of type 'string'"),
        ("/events/0/date", "nat", "invalid event date"),
        ("/events/0/date", "2015-05-17T23:18:", "invalid event date"),
        ("/projects/katsumata_clean_data", [], "[] is not of type 'object'"),
        ("/other_roles", ["hello"], "'hello' is not one of ['permanent_unprocessed']"),
    ],
)
def test_invalid_file_document_set(file_json, pointer, value, message):
    p = JsonPointer(pointer)
    p.set(file_json, value)
    with pytest.raises(ValidationError):
        File.model_validate_json(json.dumps(file_json))
