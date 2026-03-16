from elasticsearch import Elasticsearch

from config import Elasticsearch_Config
from logger import log_event
from reading_writing_es import Targets,Intel_signal
from intel_handler import Intel_handler_service
from intel_consumer import Consumer

def main():
    es =Elasticsearch(Elasticsearch_Config.HOST)

    targets = Targets(es)
    intel_signal =Intel_signal(es)
    intel_service = Intel_handler_service(
         targets=targets,
        intel_signal=intel_signal
    )

    consumer =Consumer(intel_service=intel_service)

    log_event("info","intel service ready")
    consumer.run()

if __name__ == "__main__":
    main()
