import os

class Kafka_Config:
    BOOTSTRAP_SERVERS:str = os.getenv("kafka_boostrap_server","kafka:9092")
    GROUP_ID:str = os.getenv("KAFKA_GROUP_ID","digital_group_id")
    TOPIC_INTEL:str ="intel"
    TOPIC_INTEL_DLQ:str = "intel_signals_dlq"


class Elasticsearch_Config:
    HOST:str = os.getenv("ES_HOST","http://elasticsearch:9200")
    INDEX_TARGET:str = "targets"
    INDEX_INTEL:str = "intel_signals"

class App_Config:
    PRIORITY_LEVEL:int =99
