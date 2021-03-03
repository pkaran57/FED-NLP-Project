import logging

from src.fomc.FOMCClient import FOMCClient
from src.fomc.domain.FOMCDocType import FOMCDocType

logging.basicConfig(format="'%(asctime)s' %(name)s : %(message)s'", level=logging.INFO)
logger = logging.getLogger("main")

if __name__ == "__main__":
    fomc_client = FOMCClient()
    all_materials = fomc_client.get_all_materials()

    monetary_policy_docs = [
        material
        for material in all_materials
        if material.type == FOMCDocType.POLICY_STATEMENTS.value
    ]
    logger.info("Found {} docs".format(len(monetary_policy_docs)))
    print(monetary_policy_docs[0].get_content())
