from datetime import date
from typing import List

from pydantic import Field
from pydantic.main import BaseModel

from fomc.domain.FOMCFileReference import FOMCFileReference


class FOMCDocReference(BaseModel):
    meeting_date: date = Field(..., alias='d')
    document_date: str = Field(None, alias='dt')
    type: str
    url: str = None
    files: List[FOMCFileReference] = None
