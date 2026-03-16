from datetime import datetime

from config import App_Config
from models import IntelSignal
from reading_writing_es import Targets, Intel_signal
from haversine import haversine_km
from logger import log_event


class Intel_handler_service:
    def __init__(self,
                 targets: Targets,
                 intel_signal: Intel_signal):
        self.targets = targets
        self.intel = intel_signal

    def process(self, signal: IntelSignal):
        log_event("INFO", "process inter signal")

        target = self.targets.get_target(signal.entity_id)
        temp = {}

        if target is None:
            temp["priority_level"] = App_Config.PRIORITY_LEVEL
            temp["distance_from_last_km"] = 0.0
            temp["avg_speed"] = None

            self.targets.upsert_target(
                signal.entity_id,
                {
                    "entity_id": signal.entity_id,
                    "priority_level": App_Config.PRIORITY_LEVEL,
                    "last_lon": signal.reported_lon,
                    "last_let": signal.reported_lat,
                    "last_timestamp": signal.timestamp,
                    "status": "unknown",
                },
            )

        else:
            distance_km = self.calculate_distance(signal,target)
            avg_speed =self.calculate_avg_speed(signal,target,distance_km)

            temp["distance_from_last_km"] = distance_km
            temp["avg_speed"] = avg_speed

            self.targets.update_target_location(
                entity_id=signal.entity_id,
                new_lat=float(signal.reported_lat),
                new_lon=float(signal.reported_lon),
                timestamp=signal.timestamp,
                distance_km=distance_km,
                avg_speed=avg_speed,
            )
        self.intel.save(signal,temp)
        log_event("INFO","intel signal complete")

    def calculate_distance(self, signal: IntelSignal, target):
        last_let = target.get("last_lat")
        last_lon = target.get("last_lon")

        if last_lon is None or last_let is None:
            log_event("DEBUG", "no previous location for entity")
            return 0

        distance_km = haversine_km(last_let, last_lon, float(signal.reported_lat), float(signal.reported_lon))
        log_event("DEBUG", "distance calculated")
        return distance_km

    def calculate_avg_speed(self, signal: IntelSignal, target, distance_km):
        last_timestamp = target.get("last_timestamp")
        if not last_timestamp:
            return None
        try:
            t1 = datetime.fromisoformat(last_timestamp)
            t2 = datetime.fromisoformat(signal.timestamp)
            seconds = (t2 - t1).total_seconds()

            if seconds <= 0:
                return None
            avg_speed = (distance_km * 1000) / seconds
            log_event("DEBUG", "avg_speed_calculate")
            return avg_speed
        except Exception as e:
            log_event("ERROR", "not calculate speed")
            return None
