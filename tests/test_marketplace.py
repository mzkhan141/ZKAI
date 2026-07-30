"""Tests for AI Marketplace."""

import pytest
from zkai.marketplace.marketplace import Marketplace, MarketplaceItem, MarketplacePublisher


def test_marketplace_operations():
    mp = Marketplace()
    items = mp.search("code", category="applications")
    assert len(items) >= 1
    assert items[0].name == "CodeStudio App"

    downloaded = mp.client.download(items[0].item_id)
    assert downloaded is not None
    assert downloaded.download_count == 1

    new_rating = mp.client.rate(items[0].item_id, 4.0)
    assert new_rating == 4.5

    new_item = MarketplaceItem(
        item_id="custom_pack_1",
        name="Knowledge Pack Alpha",
        version="1.0.0",
        category="knowledge_packs",
        description="Docs on quantum computing",
        author="Contributor",
    )
    mp.publisher.publish(new_item)
    mp.items[new_item.item_id] = new_item
    assert mp.get_item("custom_pack_1") is not None
