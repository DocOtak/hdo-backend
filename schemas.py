import json
from enum import Enum

from pydantic import BaseModel, ConfigDict, Field, EmailStr
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



class Cruise(BaseModel):
    model_config = ConfigDict(extra="forbid")

    expocode: str = Field(examples=["318M20130321"])
    ship: str
    participants: list[Participant]
    files: set[int]
    cf_robots: set[CFRobotEnum] = set()

    description: str | SkipJsonSchema[None] = Field(None, json_schema_extra=pop_default_from_schema)
    license: License | SkipJsonSchema[None] = Field(None, json_schema_extra=pop_default_from_schema)

main_model_schema = Cruise.model_json_schema()
print(json.dumps(main_model_schema, indent=2))