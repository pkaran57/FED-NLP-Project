import json
from typing import List
from urllib.parse import urljoin

import requests

from src.definitions import FOMC_HOST_BASE_URL
from src.fomc.domain.FOMCDocReference import FOMCDocReference


class FOMCClient:
    _BASE_URL = f"{FOMC_HOST_BASE_URL}/monetarypolicy/materials/assets/"

    def getdoc_types(self):
        url = urljoin(self._BASE_URL, "doctypes.json")
        response = requests.get(url)
        assert response.ok
        return json.loads(response.content)

    def get_historical_materials(self) -> List[FOMCDocReference]:
        url = urljoin(self._BASE_URL, "final-hist.json")
        response = requests.get(url)
        assert response.ok
        materials = list(map(FOMCDocReference.parse_obj, response.json()["mtgitems"]))
        return self._get_fomc_docs_sorted_by_date(materials)

    def get_recent_materials(self) -> List[FOMCDocReference]:
        url = urljoin(self._BASE_URL, "final-recent.json")
        response = requests.get(url)
        assert response.ok
        materials = list(map(FOMCDocReference.parse_obj, response.json()["mtgitems"]))
        return self._get_fomc_docs_sorted_by_date(materials)

    def get_all_materials(self) -> List[FOMCDocReference]:
        recent_materials = self.get_recent_materials()
        historical_materials = self.get_historical_materials()

        return self._get_fomc_docs_sorted_by_date(
            recent_materials + historical_materials
        )

    @staticmethod
    def _get_fomc_docs_sorted_by_date(docs):
        return sorted(docs, key=lambda docRef: docRef.meeting_date, reverse=True)
