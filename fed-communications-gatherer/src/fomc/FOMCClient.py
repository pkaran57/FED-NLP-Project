import json
from urllib.parse import urljoin

import requests

from fomc.domain.FOMCDocReference import FOMCDocReference


class FOMCClient:
    _BASE_URL = 'https://www.federalreserve.gov/monetarypolicy/materials/assets/'

    def getdoc_types(self):
        url = urljoin(self._BASE_URL, 'doctypes.json')
        response = requests.get(url)
        assert response.ok
        return json.loads(response.content)

    def get_all_materials(self):
        url = urljoin(self._BASE_URL, 'final-hist.json')
        response = requests.get(url)
        assert response.ok
        return list(map(FOMCDocReference.parse_obj, response.json()['mtgitems']))
