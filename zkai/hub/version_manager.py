"""HubVersionManager for model semver releases."""

class HubVersionManager:
    """Manages semantic version releases for published models."""

    @staticmethod
    def compare_versions(v1: str, v2: str) -> int:
        p1 = [int(x) for x in v1.split(".")]
        p2 = [int(x) for x in v2.split(".")]
        return (p1 > p2) - (p1 < p2)
