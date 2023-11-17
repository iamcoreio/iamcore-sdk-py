import unittest

from iamcore.client.auth import get_token_with_password
from iamcore.client.exceptions import IAMUnauthorizedException
from iamcore.client.conf import SYSTEM_BACKEND_CLIENT_ID
from tests.conf import IAMCORE_ROOT_USER, IAMCORE_ROOT_PASSWORD


class GetTokenTestCase(unittest.TestCase):
    def test_token_with_password_ok(self) -> None:
        credentials = get_token_with_password("root", SYSTEM_BACKEND_CLIENT_ID,
                                              IAMCORE_ROOT_USER, IAMCORE_ROOT_PASSWORD)
        self.assertTrue(bool(credentials.access_token))
        self.assertTrue(bool(credentials.refresh_token))
        self.assertTrue(bool(credentials.scope))
        self.assertTrue(bool(credentials.token_type))
        self.assertTrue(bool(credentials.session_state))

    def test_token_with_password_fail(self) -> None:
        with self.assertRaises(IAMUnauthorizedException) as context:
            get_token_with_password("root", SYSTEM_BACKEND_CLIENT_ID, IAMCORE_ROOT_USER, 'nopassword')
        self.assertTrue('Unauthorized:' in context.exception.msg)

