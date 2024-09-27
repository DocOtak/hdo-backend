import json
from enum import Enum
from datetime import datetime, date
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, EmailStr, constr
from pydantic.json_schema import SkipJsonSchema

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


class Cruise(BaseModel):
    model_config = ConfigDict(extra="forbid")

    expocode: str = Field(examples=["318M20130321"])
    ship: str
    participants: list[Participant]
    files: set[int]
    notes: list[Note]
    collections: Collections

    startDate: date | Literal[""]
    startEdate: date | Literal[""]

    # optional things here
    cf_robots: set[CFRobotEnum] = set()
    description: str | SkipJsonSchema[None] = Field(None, json_schema_extra=pop_default_from_schema)
    license: License | SkipJsonSchema[None] = Field(None, json_schema_extra=pop_default_from_schema)
    sites: Sites | SkipJsonSchema[None] = Field(None, json_schema_extra=pop_default_from_schema)

main_model_schema = Cruise.model_json_schema()
print(json.dumps(main_model_schema, indent=2))