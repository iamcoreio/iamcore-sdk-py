import pytest
from pydantic import ValidationError

from iamcore.client.config import BaseConfig


class TestBaseConfig:
    """Tests for BaseConfig class."""

    def test_config_from_env_vars(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """Test configuration loading from environment variables."""
        monkeypatch.setenv("IAMCORE_URL", "https://api.example.com")
        monkeypatch.setenv("IAMCORE_ISSUER_URL", "https://auth.example.com")
        monkeypatch.setenv("SYSTEM_BACKEND_CLIENT_ID", "test-client-id")
        monkeypatch.setenv("IAMCORE_CLIENT_TIMEOUT", "60")

        config = BaseConfig()

        assert str(config.iamcore_url) == "https://api.example.com/"
        assert str(config.iamcore_issuer_url) == "https://auth.example.com/"
        assert config.system_backend_client_id == "test-client-id"
        assert config.iamcore_client_timeout == 60

    def test_config_default_timeout(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """Test configuration with default timeout."""
        monkeypatch.setenv("IAMCORE_URL", "https://api.example.com")
        monkeypatch.setenv("IAMCORE_ISSUER_URL", "https://auth.example.com")
        monkeypatch.setenv("SYSTEM_BACKEND_CLIENT_ID", "test-client-id")

        config = BaseConfig()

        assert config.iamcore_client_timeout == 30

    def test_config_manual_set(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """Test manual configuration setting."""
        monkeypatch.setenv("IAMCORE_URL", "https://api.example.com")
        monkeypatch.setenv("IAMCORE_ISSUER_URL", "https://auth.example.com")
        monkeypatch.setenv("SYSTEM_BACKEND_CLIENT_ID", "test-client-id")

        config = BaseConfig()

        # Override with manual config
        config.set_iamcore_config(
            iamcore_url="https://manual.example.com",
            iamcore_issuer_url="https://manual-auth.example.com",
            client_id="manual-client-id",
        )

        assert str(config.iamcore_url) == "https://manual.example.com/"
        assert str(config.iamcore_issuer_url) == "https://manual-auth.example.com/"
        assert config.system_backend_client_id == "manual-client-id"

    def test_config_invalid_url(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """Test configuration with invalid URL."""
        monkeypatch.setenv("IAMCORE_URL", "not-a-url")
        monkeypatch.setenv("IAMCORE_ISSUER_URL", "https://auth.example.com")
        monkeypatch.setenv("SYSTEM_BACKEND_CLIENT_ID", "test-client-id")

        with pytest.raises(ValidationError) as exc_info:
            BaseConfig()

        assert "iamcore_url" in str(exc_info.value)

    def test_config_missing_required_fields(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """Test configuration with missing required fields."""
        monkeypatch.setenv("IAMCORE_URL", "https://api.example.com")
        # Missing IAMCORE_ISSUER_URL and SYSTEM_BACKEND_CLIENT_ID

        with pytest.raises(ValidationError) as exc_info:
            BaseConfig()

        error_str = str(exc_info.value)
        assert "iamcore_issuer_url" in error_str
        assert "system_backend_client_id" in error_str

    def test_config_timeout_validation(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """Test configuration timeout validation."""
        monkeypatch.setenv("IAMCORE_URL", "https://api.example.com")
        monkeypatch.setenv("IAMCORE_ISSUER_URL", "https://auth.example.com")
        monkeypatch.setenv("SYSTEM_BACKEND_CLIENT_ID", "test-client-id")
        monkeypatch.setenv("IAMCORE_CLIENT_TIMEOUT", "0")  # Invalid: too low

        with pytest.raises(ValidationError) as exc_info:
            BaseConfig()

        assert "iamcore_client_timeout" in str(exc_info.value)

    def test_config_timeout_too_high(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """Test configuration timeout validation for too high value."""
        monkeypatch.setenv("IAMCORE_URL", "https://api.example.com")
        monkeypatch.setenv("IAMCORE_ISSUER_URL", "https://auth.example.com")
        monkeypatch.setenv("SYSTEM_BACKEND_CLIENT_ID", "test-client-id")
        monkeypatch.setenv("IAMCORE_CLIENT_TIMEOUT", "400")  # Invalid: too high

        with pytest.raises(ValidationError) as exc_info:
            BaseConfig()

        assert "iamcore_client_timeout" in str(exc_info.value)

    def test_config_case_insensitive_env_vars(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """Test that environment variables are case insensitive."""
        monkeypatch.setenv("iamcore_url", "https://api.example.com")  # lowercase
        monkeypatch.setenv("IAMCORE_ISSUER_URL", "https://auth.example.com")  # uppercase
        monkeypatch.setenv("system_backend_client_id", "test-client-id")  # lowercase

        config = BaseConfig()

        assert str(config.iamcore_url) == "https://api.example.com/"
        assert str(config.iamcore_issuer_url) == "https://auth.example.com/"
        assert config.system_backend_client_id == "test-client-id"

    def test_config_url_with_trailing_slash(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """Test that URLs with trailing slashes are handled correctly."""
        monkeypatch.setenv("IAMCORE_URL", "https://api.example.com/")
        monkeypatch.setenv("IAMCORE_ISSUER_URL", "https://auth.example.com/")
        monkeypatch.setenv("SYSTEM_BACKEND_CLIENT_ID", "test-client-id")

        config = BaseConfig()

        # HttpUrl normalizes URLs
        assert str(config.iamcore_url) == "https://api.example.com/"
        assert str(config.iamcore_issuer_url) == "https://auth.example.com/"

    def test_config_string_properties(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """Test that string properties return correct values."""
        monkeypatch.setenv("IAMCORE_URL", "https://api.example.com")
        monkeypatch.setenv("IAMCORE_ISSUER_URL", "https://auth.example.com")
        monkeypatch.setenv("SYSTEM_BACKEND_CLIENT_ID", "test-client-id")

        config = BaseConfig()

        assert config.iamcore_url_str == "https://api.example.com/"
        assert config.iamcore_issuer_url_str == "https://auth.example.com/"
