from fomc.FOMCClient import FOMCClient
from fomc.domain.FOMCDocType import FOMCDocType

if __name__ == '__main__':
    fomc_client = FOMCClient()
    all_materials = fomc_client.get_all_materials()

    monetary_policy_docs = [material for material in all_materials if material.type == FOMCDocType.POLICY_STATEMENTS.value]
    print(len(monetary_policy_docs))
    print(monetary_policy_docs[0].get_html_doc_url())
