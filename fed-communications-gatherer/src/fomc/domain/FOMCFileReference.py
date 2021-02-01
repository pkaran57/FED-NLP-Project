from pydantic import Field
from pydantic.main import BaseModel


class FOMCFileReference(BaseModel):
    format: str = Field(None, alias='name')
    url: str
