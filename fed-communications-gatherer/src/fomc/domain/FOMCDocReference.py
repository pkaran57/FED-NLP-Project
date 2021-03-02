from bs4 import BeautifulSoup
from datetime import date
from pydantic import Field
from pydantic.main import BaseModel
from typing import List
from urllib.request import urlopen

from src.fomc.domain.FOMCDocType import FOMCDocType
from src.fomc.domain.FOMCFileReference import FOMCFileReference


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

    def get_content(self):
        if self.type == FOMCDocType.POLICY_STATEMENTS.value:
            html = urlopen(self.get_html_doc_url())
            soup = BeautifulSoup(html, 'lxml')

            paragraphs = soup.find("div", {"class": 'col-xs-12 col-sm-8 col-md-8'}).find_all('p')

            return [paragraph.text for paragraph in paragraphs]
        else:
            raise NotImplementedError('Method not implemented for doc type - ' + self.type)
