import logging
import os
from os import listdir

from tqdm import tqdm

from src.definitions import POLICY_STATEMENTS_OUTPUT_DIR
from src.fomc.FOMCClient import FOMCClient
from src.fomc.FOMCDoc import FOMCDoc

logging.basicConfig(format="'%(asctime)s' %(name)s : %(message)s'", level=logging.INFO)
logger = logging.getLogger("main")


def export_fomc_docs(all_materials, doc_type, output_dir):
    filtered_docs_by_type = [
        material for material in all_materials if material.type == doc_type.value
    ]
    logger.info(
        "Found {} documents of type {}. Exporting them to disk ...".format(
            len(filtered_docs_by_type), doc_type
        )
    )
    for doc in tqdm(filtered_docs_by_type):
        doc.get_fomc_Doc().export_to_disk(output_dir)


def read_fomc_docs(dir):
    fomc_docs = []
    json_files = [file for file in listdir(dir) if file.endswith(".json")]

    logger.info("Found {} documents. Reading them into memory ...")
    for file in tqdm(json_files):
        file_path = os.path.join(dir, file)
        fomc_docs.append(FOMCDoc.parse_file(file_path))

    return fomc_docs


if __name__ == "__main__":
    fomc_client = FOMCClient()
    all_materials = fomc_client.get_all_materials()

    # export_fomc_docs(all_materials, FOMCDocType.POLICY_STATEMENTS, POLICY_STATEMENTS_OUTPUT_DIR)
    fomc_docs = read_fomc_docs(POLICY_STATEMENTS_OUTPUT_DIR)
