import json
from datetime import date, datetime
from enum import Enum, StrEnum
from importlib import resources
from typing import Annotated, Any, Literal, NamedTuple

from pydantic import BaseModel, ConfigDict, EmailStr, Field, constr
from pydantic.json_schema import SkipJsonSchema

from cchdo.hdo_backend import data

_iso31661 = json.loads(resources.files(data).joinpath("iso-3166-1.json").read_text())
_iso31663 = json.loads(resources.files(data).joinpath("iso-3166-3.json").read_text())
_allowed_county_codes = [c["alpha-2"] for c in _iso31661]
_allowed_county_codes.extend([c["alpha-4"] for c in _iso31663])
# emptry string country is OK too
_allowed_county_codes.append("")

CountryEnum = StrEnum("CountryEnum", names=((country, country) if country != "" else ("Empty", "") for country in _allowed_county_codes))

# https://skaaptjop.medium.com/how-i-use-pydantic-unrequired-fields-so-that-the-schema-works-0010d8758072
def pop_default_from_schema(s):
    s.pop('default', None)

class LicenseEnum(Enum):
    PDM10 = "PDM 1.0"
    CCBY40 = "CC BY 4.0"
    CCBY30 = "CC BY 3.0"
    CCBY20 = "CC BY 2.0"
    CCBY10 = "CC BY 1.0"

class License(BaseModel):
    license: LicenseEnum
    name: str = Field(min_length=1)
    email: EmailStr
    institution: str = Field(min_length=1)

class CFRobotEnum(Enum):
    BOTTLE = "bottle"
    CTD = "ctd"
    SUMMARY = "summary"

class Participant(BaseModel):
    model_config = ConfigDict(extra="forbid")

    name: str
    role: str
    institution: str = ""
    email: str = ""

class Note(BaseModel):
    model_config = ConfigDict(extra="forbid")

    name: str
    data_type: str
    action: str
    summary: str
    date: datetime
    body: list[str]

class Collections(BaseModel):
    model_config = ConfigDict(extra="forbid")

    woce_lines: set[constr(min_length=1, pattern=r"^\S")]
    programs: set[constr(min_length=1, pattern=r"^\S")]
    oceans: set[constr(min_length=1, pattern=r"^\S")]
    groups: set[constr(min_length=1, pattern=r"^\S")]

class Sites(BaseModel):
    model_config = ConfigDict(extra="forbid")

    microstructure_ucsd_edu: dict | SkipJsonSchema[None] = Field(None, json_schema_extra=pop_default_from_schema, alias="microstructure.ucsd.edu")
    dimes_ucsd_edu: dict | SkipJsonSchema[None] = Field(None, json_schema_extra=pop_default_from_schema, alias="dimes.ucsd.edu")

class ReferenceType(Enum):
    DOI = "doi"
    ARK = "ark"
    ALIAS = "alias"
    ACCESSION = "accession"
    CITATION = "citation"
    LINK = "link"
    RELATED = "related"
    FLOAT = "float"

class References(BaseModel):
    model_config = ConfigDict(extra="forbid")

    organization: str
    type: ReferenceType
    value: str
    properties: dict[str, Any]

class Point2D(NamedTuple):
    longitude: float
    latitude: float

class LineString(BaseModel):
    model_config = ConfigDict(extra="forbid")
    type: Literal["LineString"]
    coordinates: Annotated[list[Point2D], Field(min_length=2)]

class Empty(BaseModel):
    model_config = ConfigDict(extra="forbid")

    ...

class Geometry(BaseModel):
    model_config = ConfigDict(extra="forbid")

    track: LineString | Empty

class Cruise(BaseModel):
    model_config = ConfigDict(extra="forbid")

    expocode: str = Field(examples=["318M20130321"])
    ship: str
    participants: list[Participant]
    files: set[int]
    notes: list[Note]
    collections: Collections

    startDate: date | Literal[""]
    endDate: date | Literal[""]

    country: CountryEnum

    geometry: Geometry

    # optional things here
    cf_robots: set[CFRobotEnum] = set()
    description: str | SkipJsonSchema[None] = Field(None, json_schema_extra=pop_default_from_schema)
    license: License | SkipJsonSchema[None] = Field(None, json_schema_extra=pop_default_from_schema)
    sites: Sites | SkipJsonSchema[None] = Field(None, json_schema_extra=pop_default_from_schema)

    start_port: str | SkipJsonSchema[None] = Field(None, json_schema_extra=pop_default_from_schema)
    end_port: str | SkipJsonSchema[None] = Field(None, json_schema_extra=pop_default_from_schema)

    references: list[References] | SkipJsonSchema[None] = Field(None, json_schema_extra=pop_default_from_schema)

if __name__ == "__main__":
    main_model_schema = Cruise.model_json_schema()
    print(json.dumps(main_model_schema, indent=2))
