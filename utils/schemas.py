from pydantic import BaseModel
from typing import List

class IntentSchema(BaseModel):

    core_problem: str

    methodology_needed: List[str]

    domain: str

    temporal_preference: str

    expanded_queries: List[str]