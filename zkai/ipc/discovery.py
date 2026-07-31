"""ServiceDiscovery pattern for dynamic IPC endpoint resolution."""

from typing import Dict, List, Optional
from zkai.core.logger import get_logger

logger = get_logger("ipc.discovery")


class ServiceDiscovery:
    """Registry maintaining active service endpoint locations and capability attributes."""

    def __init__(self):
        self._endpoints: Dict[str, Dict[str, str]] = {}

    def register_service(self, name: str, host: str, port: int, protocol: str = "http") -> None:
        endpoint = {"host": host, "port": str(port), "protocol": protocol, "url": f"{protocol}://{host}:{port}"}
        self._endpoints[name] = endpoint
        logger.info(f"ServiceDiscovery registered endpoint '{name}' -> {endpoint['url']}")

    def unregister_service(self, name: str) -> None:
        if name in self._endpoints:
            del self._endpoints[name]

    def resolve(self, name: str) -> Optional[Dict[str, str]]:
        return self._endpoints.get(name)

    def list_services(self) -> List[str]:
        return list(self._endpoints.keys())
