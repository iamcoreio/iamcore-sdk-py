import unittest
import pytest
from iamcore.irn import IRN

from iamcore.client.auth import get_token_with_password, TokenResponse
from iamcore.client.tenant import search_tenant, create_tenant
from iamcore.client.conf import SYSTEM_BACKEND_CLIENT_ID
from iamcore.client.policy import search_policy, CreatePolicyRequest
from iamcore.client.user import CreateUser, user_attach_policies, search_all_users
from tests.conf import IAMCORE_ROOT_USER, IAMCORE_ROOT_PASSWORD


@pytest.fixture(scope="class")
def root_token(request):
    request.cls.root = get_token_with_password("root", SYSTEM_BACKEND_CLIENT_ID,
                                               IAMCORE_ROOT_USER, IAMCORE_ROOT_PASSWORD)


@pytest.fixture(scope="class")
def test_user(request):
    request.cls.tenant_name = "iamcore-py-test-policy-tenant"
    request.cls.tenant_display_name = "iamcore_ Python Sdk test policy tenant"
    request.cls.policy_name = "allow-all-iamcore-py-test-policy-CrudUserPoliciesTestCase"
    request.cls.policy_description = "Allow all for iamcore-py-test-policy-tenant tenant"
    request.cls.user_email = "py-test-user@iamcore.io"
    request.cls.user_name = "py-test-user"
    request.cls.user_password = "py-test-user"


@pytest.mark.usefixtures("root_token")
@pytest.mark.usefixtures("test_user")
class CrudUserPoliciesTestCase(unittest.TestCase):
    root: TokenResponse
    tenant_name: str
    tenant_display_name: str
    policy_name: str
    policy_description: str
    user_name: str
    user_email: str
    user_password: str

    def test_00_cleanup_ok(self):
        users = list(search_all_users(self.root.access_headers, username=self.user_name))
        if users:
            self.assertLessEqual(len(users), 1)
            for user in users:
                self.assertEqual(user.username, self.user_name)
                self.assertTrue(user.id)
                self.assertTrue(user.irn)
                self.assertEqual(user.first_name, "Test")
                self.assertEqual(user.last_name, "User")
                self.assertTrue(user.path)
                user.delete(self.root.access_headers)
        users = list(search_all_users(self.root.access_headers, username=self.user_name))
        self.assertEqual(len(users), 0)

    def test_10_crud_ok(self):
        tenants = search_tenant(self.root.access_headers, name=self.tenant_name).data
        tenant = tenants[0] if len(tenants) > 0 else \
            create_tenant(self.root.access_headers, name=self.tenant_name, display_name=self.tenant_display_name)
        self.assertTrue(tenant)
        policies = search_policy(self.root.access_headers, name=self.policy_name).data
        account = IRN.of(tenant.irn).account_id
        policy = policies[0] if len(policies) > 0 else \
            CreatePolicyRequest(self.policy_name, 'tenant', self.policy_description, tenant_id=tenant.tenant_id) \
                .with_statement('allow', self.policy_description,
                                [f"irn:{account}:unittest:{tenant.tenant_id}:*"], ['*']) \
                .create(self.root.access_headers)
        self.assertTrue(policy)
        user = CreateUser(tenant_id=tenant.tenant_id,
                          username=self.user_name,
                          email=self.user_email,
                          first_name="Test",
                          last_name="User",
                          password=self.user_password,
                          confirm_password=self.user_password,
                          path="/") \
            .create(auth_headers=self.root.access_headers)
        self.assertTrue(user)
        user_attach_policies(self.root.access_headers, user.id, [policy.id])
        # todo

    def test_90_cleanup_ok(self):
        users = list(search_all_users(self.root.access_headers, username=self.user_name))
        if users:
            self.assertLessEqual(len(users), 1)
            for user in users:
                self.assertEqual(user.username, self.user_name)
                self.assertTrue(user.id)
                self.assertTrue(user.irn)
                self.assertEqual(user.first_name, "Test")
                self.assertEqual(user.last_name, "User")
                self.assertTrue(user.path)
                user.delete(self.root.access_headers)
        users = list(search_all_users(self.root.access_headers, username=self.user_name))
        self.assertEqual(len(users), 0)
