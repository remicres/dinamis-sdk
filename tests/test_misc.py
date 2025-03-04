"""Misc test module."""

import dinamis_sdk


def test_userinfo():
    """Test userinfo method."""
    print(dinamis_sdk.get_userinfo())


def test_username():
    """Test userinfo method."""
    print(dinamis_sdk.get_username())


test_userinfo()
test_username()
