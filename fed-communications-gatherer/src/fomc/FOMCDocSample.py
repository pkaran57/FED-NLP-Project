import os

from typing import Dict

from pydantic.main import BaseModel

from src.fomc.FOMCDoc import FOMCDoc


class FOMCDocSample(BaseModel):
    fomc_doc: FOMCDoc
    entity_sentiments: Dict
    change_in_vix: float = None
    change_in_s_n_p_500: float = None

    def export_to_disk(self, export_dir):
        file_name = "{}-{}-sample.json".format(self.fomc_doc.meeting_date, self.fomc_doc.doc_type.value)
        with open(os.path.join(export_dir, file_name), "w", encoding="utf-8") as file:
            file.write(self.json())
