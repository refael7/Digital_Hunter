import json

from kafka import KafkaProducer, KafkaConsumer
from pydantic import ValidationError

from config import Kafka_Config
from models import IntelSignal
from intel_handler import Intel_handler_service
from logger import log_event


class Consumer:
    def __init__(self, intel_service: Intel_handler_service):
        self.intel_service = intel_service
        self.consumer = KafkaConsumer(
            Kafka_Config.TOPIC_INTEL,
            bootstrap_servers=Kafka_Config.BOOTSTRAP_SERVERS,
            group_id=Kafka_Config.GROUP_ID,
            value_deserializer=lambda raw: json.loads(raw.decode("utf-8")),
            auto_offset_reset="earliest",
            enable_auto_commit=True,
        )
        self.dlq_producer = KafkaProducer(
            bootstrap_servers=Kafka_Config.BOOTSTRAP_SERVERS,
            value_deserializer=lambda v: json.loads(v.decode("utf-8")),

        )

    def run(self):
        for message in self.consumer:
            raw = message.value
            self.handel(raw)

    def handel(self, raw):
        try:
            signal = IntelSignal(**raw)
        except ValidationError as e:
            log_event("ERROR", "valid filed", {"error": str(e)})
             self.send_to_dlq(raw, reason: str(e))


    def send_to_dlq(self, raw, reason):
        dlq_payload={}
        for key, value in raw.itams():
            dlq_payload[key]=value
        dlq_payload["dlq reason"]=reason
        self.dlq_producer.send(Kafka_Config.TOPIC_INTEL_DLQ,value=dlq_payload)
        self.dlq_producer.flush()
        log_event("INFO","message send to dlq")
