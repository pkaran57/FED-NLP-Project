import os
from datetime import date
from typing import List

from pydantic import BaseModel

from src.fomc.client.domain.FOMCDocType import FOMCDocType


class FOMCDoc(BaseModel):
    meeting_date: date
    paragraphs: List[str]
    doc_type: FOMCDocType

    def export_to_disk(self, export_dir):
        file_name = "{}-{}.json".format(self.meeting_date, self.doc_type.value)
        with open(os.path.join(export_dir, file_name), "w", encoding="utf-8") as file:
            file.write(self.json())

    def get_content(self):
        return " ".join(paragraph.strip() for paragraph in self.paragraphs)
