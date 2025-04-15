from pydantic import BaseModel
import datetime


class DeviceResult(BaseModel):
    """Device result class"""
    name: str
    network_id: str
    node_id: str
    status: str
    last_online: int = None
    timezone: str = None

    @classmethod
    def from_dict(cls, data: dict):
        """Create a DeviceResult instance from a dictionary"""
        name = data.get("name")
        network_id = data.get("network_id")
        node_id = data.get("node_id")
        last_online = data.get("last_online")
        clock = data.get("clock")
        status = 'unknown'
        if clock - last_online > 180000:
            status = 'offline'
        else:
            status = 'online'
        return cls(
            name=name,
            network_id=network_id,
            node_id=node_id,
            status=status,
            last_online=last_online,
            timezone=datetime.datetime.now().astimezone().tzname()
        )
