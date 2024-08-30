import json
from enum import Enum

from pydantic import BaseModel, ConfigDict

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

    expocode: str
    ship: str
    participants: list[Participant]
    files: set[int]
    cf_robots: set[CFRobotEnum] = set()

main_model_schema = Cruise.model_json_schema()
print(json.dumps(main_model_schema, indent=2))