"""HubMetadataManager for managing ModelCard metadata."""

from zkai.models.metadata import ModelMetadata


class HubMetadataManager:
    """CRUD interface for hub model metadata."""

    def __init__(self):
        self.metadata_store: dict[str, ModelMetadata] = {}

    def save_metadata(self, name: str, meta: ModelMetadata) -> None:
        self.metadata_store[name] = meta
