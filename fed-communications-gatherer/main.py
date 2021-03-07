import logging

from src.definitions import POLICY_STATEMENTS_OUTPUT_DIR
from src.fomc.FOMCCommunicationDocsService import FOMCCommunicationDocsService

logging.basicConfig(format="'%(asctime)s' %(name)s : %(message)s'", level=logging.INFO)
logger = logging.getLogger("main")

if __name__ == "__main__":
    fomc_communication_docs_service = FOMCCommunicationDocsService()

    # fomc_communication_docs_service.export_fomc_docs(
    #     FOMCDocType.POLICY_STATEMENTS, POLICY_STATEMENTS_OUTPUT_DIR
    # )
    fomc_docs = fomc_communication_docs_service.read_fomc_docs(POLICY_STATEMENTS_OUTPUT_DIR)
