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

    def get_html_doc_url(self):
        if self.files:
            html_doc_refs = [ref for ref in self.files if ref.url.endswith('.htm') or ref.url.endswith('.html')]
            if len(html_doc_refs) > 0:
                return html_doc_refs[0].get_full_url()

        return None
