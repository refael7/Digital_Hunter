from config import Elasticsearch_Config, App_Config
from models import IntelSignal
from typing import Optional
from logger import log_event
from elasticsearch import Elasticsearch, NotFoundError


class Targets:
    def __init__(self, es_client):
        self.es_client = es_client

    def get_target(self, entity_id):
        try:
            response = self.es_client.get(index=Elasticsearch_Config.INDEX_TARGET, id=entity_id)
            log_event("DEBAG", "target found in DB")
            return response["source"]
        except NotFoundError:
            log_event("WARNING", "target not found")
            return None

    def upsert_target(self, entity_id, date):
        self.es_client.index(
            index=Elasticsearch_Config.INDEX_TARGET,
            id=entity_id,
            document=date,

        )
        log_event("INFO", "target upsert in db")

    def update_target_location(self, timestamp: str,
                               entity_id: str,
                               new_lat: float,
                               new_lon: float,
                               distance_km: float,
                               avg_speed: Optional[float]):
        doc = {
            "last_let":new_lat,
            "last_lon":new_lon,
            "last_timestamp":timestamp,
            "distance_from_last_km":distance_km,
        }
        if avg_speed is not None:
            doc["avg_speed"]=avg_speed

        self.es_client.update(
            index=Elasticsearch_Config.INDEX_TARGET,
            id=entity_id,
            body={"doc":doc}
        )
        log_event("INFO","target location update")

class Intel_signal:
    def __init__(self, es_client):
        self.es_client = es_client

    def save(self,signal:IntelSignal,data):
        signal_to_dict = signal.model_dump()

        doc = {}
        for key , value in signal_to_dict.items():
            doc[key] = value
        for key , value in data.items():
            doc[key] = value

        self.es_client.index(
            index=Elasticsearch_Config.INDEX_TARGET,
            id=signal.signal_id,
            document=doc,
        )
        log_event("INFO","intel signal saved")
