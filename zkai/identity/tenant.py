"""Multi-Tenant OS Infrastructure, Tenant Manager, Workspace Isolation, and Tenant Security for ZKAI."""

from dataclasses import dataclass, field
import uuid
from typing import Any, Dict, List, Optional
from zkai.core.logger import get_logger

logger = get_logger("identity.tenant")


@dataclass
class Tenant:
    tenant_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    name: str = "default_tenant"
    tier: str = "personal"  # personal, team, enterprise, cloud
    max_workspaces: int = 5
    max_users: int = 10
    allocated_quota_mb: float = 10240.0


class WorkspaceIsolation:
    """Enforces logical and storage workspace isolation between tenants."""

    def __init__(self):
        self.workspace_map: Dict[str, str] = {}  # workspace_id -> tenant_id

    def bind(self, workspace_id: str, tenant_id: str) -> None:
        self.workspace_map[workspace_id] = tenant_id

    def validate_access(self, tenant_id: str, workspace_id: str) -> bool:
        owner = self.workspace_map.get(workspace_id)
        if owner and owner != tenant_id:
            logger.warning(f"WorkspaceIsolation DENIED tenant '{tenant_id}' access to workspace '{workspace_id}' owned by '{owner}'")
            return False
        return True


class SharedKnowledge:
    """Controlled cross-tenant knowledge sharing with capability permissions."""

    def __init__(self):
        self.shared_resources: Dict[str, List[str]] = {}  # resource_id -> list of granted_tenant_ids

    def share_resource(self, resource_id: str, target_tenant_id: str) -> None:
        if resource_id not in self.shared_resources:
            self.shared_resources[resource_id] = []
        self.shared_resources[resource_id].append(target_tenant_id)

    def can_access(self, resource_id: str, tenant_id: str) -> bool:
        grants = self.shared_resources.get(resource_id, [])
        return tenant_id in grants


class OrganizationPolicies:
    """Per-organization security and operational policy rules."""

    def __init__(self):
        self.policies: Dict[str, Dict[str, Any]] = {}

    def set_policy(self, org_id: str, policy_name: str, value: Any) -> None:
        if org_id not in self.policies:
            self.policies[org_id] = {}
        self.policies[org_id][policy_name] = value

    def get_policy(self, org_id: str, policy_name: str, default: Any = None) -> Any:
        return self.policies.get(org_id, {}).get(policy_name, default)


class DelegatedAdministration:
    """Delegated admin roles within enterprise tenant organizations."""

    def __init__(self):
        self.admins: Dict[str, List[str]] = {}  # tenant_id -> list of admin_user_ids

    def add_admin(self, tenant_id: str, user_id: str) -> None:
        if tenant_id not in self.admins:
            self.admins[tenant_id] = []
        self.admins[tenant_id].append(user_id)

    def is_admin(self, tenant_id: str, user_id: str) -> bool:
        return user_id in self.admins.get(tenant_id, [])


class OrganizationHierarchy:
    """Nested organization structure (parent-child organizations)."""

    def __init__(self):
        self.parent_map: Dict[str, str] = {}  # child_org_id -> parent_org_id

    def set_parent(self, child_org_id: str, parent_org_id: str) -> None:
        self.parent_map[child_org_id] = parent_org_id


class QuotaManager:
    """Per-tenant resource quota manager."""

    def __init__(self):
        self.quotas: Dict[str, Dict[str, float]] = {}

    def set_quota(self, tenant_id: str, resource: str, limit: float) -> None:
        if tenant_id not in self.quotas:
            self.quotas[tenant_id] = {}
        self.quotas[tenant_id][resource] = limit


class BillingHooks:
    """Hooks for usage tracking and billing integration."""

    @staticmethod
    def record_metered_usage(tenant_id: str, metric: str, amount: float) -> None:
        logger.info(f"BillingHooks recorded metered usage for tenant '{tenant_id}': {metric}={amount}")


class ResourceIsolation:
    """Enforces compute and storage isolation boundaries across tenants."""

    @staticmethod
    def validate_boundary(requesting_tenant_id: str, target_resource_tenant_id: str) -> bool:
        return requesting_tenant_id == target_resource_tenant_id


class TenantSecurity:
    """Tenant-specific encryption key and security token isolation."""

    def __init__(self):
        self.keys: Dict[str, str] = {}

    def generate_tenant_key(self, tenant_id: str) -> str:
        key = f"key_{tenant_id}_{uuid.uuid4().hex[:8]}"
        self.keys[tenant_id] = key
        return key


class CrossTenantPolicies:
    """Policies governing cross-tenant interactions and data access."""

    @staticmethod
    def is_interaction_allowed(tenant_a: str, tenant_b: str) -> bool:
        return tenant_a == tenant_b


class TenantManager:
    """Master Multi-Tenant OS Manager overseeing tenant creation, isolation, policies, and security."""

    def __init__(self):
        self.tenants: Dict[str, Tenant] = {}
        self.isolation = WorkspaceIsolation()
        self.shared_knowledge = SharedKnowledge()
        self.policies = OrganizationPolicies()
        self.delegated_admin = DelegatedAdministration()
        self.hierarchy = OrganizationHierarchy()
        self.quota = QuotaManager()
        self.security = TenantSecurity()

    def create_tenant(self, name: str, tier: str = "personal") -> Tenant:
        tenant = Tenant(name=name, tier=tier)
        self.tenants[tenant.tenant_id] = tenant
        self.security.generate_tenant_key(tenant.tenant_id)
        logger.info(f"TenantManager created tenant '{name}' ({tenant.tenant_id}, Tier: {tier})")
        return tenant

    def get_tenant(self, tenant_id: str) -> Optional[Tenant]:
        return self.tenants.get(tenant_id)
