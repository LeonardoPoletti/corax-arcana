# test_config.py - verifies app/config.py can load required settings

from app.config import get_settings


def test_get_settings_reads_database_and_redis_url():
    # get_settings() should successfully build a Settings object with
    # database_url and redis_url populated - either from a real env var
    # or from the .env file. If it can't find them, pydantic raises a
    # ValidationError instead of returning an object, which is exactly
    # the crash we just saw on the command line.
    settings = get_settings()

    assert settings.database_url
    assert settings.redis_url
