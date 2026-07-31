"""Marketplace, MarketplaceClient, and MarketplacePublisher for ZKAI."""

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional
from zkai.hub.hub import ModelHub
from zkai.core.logger import get_logger

logger = get_logger("marketplace")


@dataclass
class MarketplaceItem:
    item_id: str
    name: str
    version: str
    category: str  # applications, agents, plugins, models, prompt_packs, workflow_packs, knowledge_packs, datasets, templates, themes
    description: str
    author: str
    rating: float = 5.0
    download_count: int = 0
    signature: str = "valid_sig"


class MarketplacePublisher:
    """Publishes artifacts and packs to the ZKAI Marketplace."""

    @staticmethod
    def publish(item: MarketplaceItem) -> str:
        logger.info(f"Published marketplace item '{item.name}' ({item.category}) v{item.version}")
        return item.item_id


class MarketplaceClient:
    """Client for browsing, searching, rating, and downloading Marketplace items."""

    def __init__(self, marketplace: "Marketplace"):
        self.marketplace = marketplace

    def download(self, item_id: str) -> Optional[MarketplaceItem]:
        item = self.marketplace.get_item(item_id)
        if item:
            item.download_count += 1
            logger.info(f"Downloaded marketplace item '{item.name}'")
        return item

    def rate(self, item_id: str, rating: float) -> float:
        item = self.marketplace.get_item(item_id)
        if item:
            item.rating = (item.rating + rating) / 2.0
            return item.rating
        return 0.0


class Marketplace:
    """Master Marketplace system architecture."""

    def __init__(self):
        self.model_hub = ModelHub()
        self.items: Dict[str, MarketplaceItem] = {}
        self.publisher = MarketplacePublisher()
        self.client = MarketplaceClient(self)
        self._seed_default_items()

    def _seed_default_items(self) -> None:
        defaults = [
            MarketplaceItem("app_1", "CodeStudio App", "1.0.0", "applications", "IDE for AI code generation", "ZKAI Team"),
            MarketplaceItem("agent_1", "Autonomous Researcher", "1.0.0", "agents", "Multi-step web research agent", "ZKAI Team"),
            MarketplaceItem("prompt_1", "Coding Prompt Pack", "1.0.0", "prompt_packs", "Curated prompts for code synthesis", "Community"),
            MarketplaceItem("flow_1", "Data Analysis Workflow Pack", "1.0.0", "workflow_packs", "DAG workflows for CSV parsing", "Community"),
        ]
        for d in defaults:
            self.items[d.item_id] = d

    def get_item(self, item_id: str) -> Optional[MarketplaceItem]:
        return self.items.get(item_id)

    def search(self, query: str, category: Optional[str] = None) -> List[MarketplaceItem]:
        results = []
        for item in self.items.values():
            if category and item.category != category:
                continue
            if query.lower() in item.name.lower() or query.lower() in item.description.lower():
                results.append(item)
        return results
