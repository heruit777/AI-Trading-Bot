from backend.brokers.dummy_broker import Dummy_Broker
from backend.brokers.upstoxBroker import UpstoxBroker
from backend.brokers.broker import Broker
from enum import Enum

class BrokerType(Enum):
    UPSTOX = "upstox"
    DUMMY = "dummy"

class BrokerFactory():
    @staticmethod
    def create_broker(broker_type: BrokerType, access_token: str, api_version: str) -> Broker:
        if broker_type == BrokerType.DUMMY:
            return Dummy_Broker(access_token, api_version)
        elif broker_type == BrokerType.UPSTOX:
            return UpstoxBroker(access_token, api_version)
        else:
            raise ValueError(f"Unknown broker type: {broker_type}")