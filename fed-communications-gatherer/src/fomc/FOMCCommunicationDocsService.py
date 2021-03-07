import logging
import os
from os import listdir
from typing import List

from tqdm import tqdm

from src.fomc.FOMCDoc import FOMCDoc
from src.fomc.client.FOMCClient import FOMCClient


class FOMCCommunicationDocsService:
    _logger = logging.getLogger("FOMCCommunicationDocsService")

    def __init__(self):
        self._client = FOMCClient()

    def export_fomc_docs(self, doc_type, output_dir) -> None:
        all_materials = self._client.get_all_materials()

        filtered_docs_by_type = [
            material for material in all_materials if material.type == doc_type.value
        ]
        self._logger.info(
            "Found {} documents of type {}. Exporting them to disk ...".format(
                len(filtered_docs_by_type), doc_type
            )
        )
        for doc in tqdm(filtered_docs_by_type):
            doc.get_fomc_Doc().export_to_disk(output_dir)

    def read_fomc_docs(self, dir) -> List[FOMCDoc]:
        fomc_docs = []
        json_files = [file for file in listdir(dir) if file.endswith(".json")]

        self._logger.info("Found {} documents. Reading them into memory ...")
        for file in tqdm(json_files):
            file_path = os.path.join(dir, file)
            fomc_docs.append(FOMCDoc.parse_file(file_path))

        return fomc_docs
