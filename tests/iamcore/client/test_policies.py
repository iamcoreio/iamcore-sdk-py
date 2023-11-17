import unittest
import pytest

from iamcore.client.auth import get_token_with_password, TokenResponse
from iamcore.client.tenant import search_tenant, create_tenant
from iamcore.client.conf import SYSTEM_BACKEND_CLIENT_ID
from iamcore.client.policy import search_policy, CreatePolicyRequest
from tests.conf import IAMCORE_ROOT_USER, IAMCORE_ROOT_PASSWORD


@pytest.fixture(scope="class")
def root_token(request):
    request.cls.root = get_token_with_password("root", SYSTEM_BACKEND_CLIENT_ID,
                                               IAMCORE_ROOT_USER, IAMCORE_ROOT_PASSWORD)


@pytest.fixture(scope="class")
def test_tenant(request):
    request.cls.tenant_name = "iamcore-py-test-policy-tenant"
    request.cls.tenant_display_name = "iamcore_ Python Sdk test policy tenant"
    request.cls.policy_name = "allow-all-iamcore-py-test-policy-tenant"
    request.cls.policy_description = "Allow all for iamcore-py-test-policy-tenant tenant"


@pytest.mark.usefixtures("root_token")
@pytest.mark.usefixtures("test_tenant")
class CrudPoliciesTestCase(unittest.TestCase):
    root: TokenResponse
    tenant_name: str
    tenant_display_name: str
    policy_name: str
    policy_description: str

    def test_00_cleanup_ok(self):
        policies = search_policy(self.root.access_headers, name=self.policy_name).data
        if policies:
            self.assertLessEqual(len(policies), 1)
            for policy in policies:
                self.assertEqual(policy.name, self.policy_name)
                self.assertTrue(policy.id)
                self.assertTrue(policy.irn)
                self.assertTrue(policy.description)
                policy.delete(self.root.access_headers)
        policies = search_policy(self.root.access_headers, name=self.policy_name)
        self.assertEqual(len(policies.data), 0)

    def test_10_crud_ok(self):
        tenants = search_tenant(self.root.access_headers, name=self.tenant_name).data
        tenant = tenants[0] if len(tenants) > 0 else \
            create_tenant(self.root.access_headers, name=self.tenant_name, display_name=self.tenant_display_name)

        policy_req = CreatePolicyRequest(self.policy_name, 'tenant', self.policy_description)
        policy_req \
            .with_statement('allow', self.policy_description, [f"irn:root:iamcore:{tenant.tenant_id}:*"], ['*']) \
            .create(self.root.access_headers)

        policies = search_policy(self.root.access_headers, name=self.policy_name).data
        if policies:
            self.assertEqual(len(policies), 1)
            created_policy = policies[0]

            self.assertEqual(created_policy.name, self.policy_name)
            self.assertEqual(created_policy.description, self.policy_description)

            self.assertTrue(created_policy.id)
            self.assertTrue(created_policy.irn)
            self.assertTrue(created_policy.statements)

    def test_90_cleanup_ok(self):
        policies = search_policy(self.root.access_headers, name=self.policy_name).data
        if policies:
            self.assertEqual(len(policies), 1)
            for policy in policies:
                self.assertEqual(policy.name, self.policy_name)
                self.assertTrue(policy.id)
                self.assertTrue(policy.irn)
                self.assertTrue(policy.description)
                policy.delete(self.root.access_headers)
        policies = search_policy(self.root.access_headers, name=self.policy_name).data
        self.assertEqual(len(policies), 0)
