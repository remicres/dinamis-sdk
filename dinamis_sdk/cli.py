"""Dinamis Command Line Interface."""

# pylint: disable=missing-function-docstring

from typing import Dict, List

import click

from .model import ApiKey, ApiKeyStorage
from .http import OAuth2ConnectionMethod
from .utils import get_logger_for, create_session

log = get_logger_for(__name__)
conn = OAuth2ConnectionMethod()


CLI_DOCSTRING = """
Dinamis SDK CLI tool.

This tool allows to manage API keys on the local machine (usually stored in ~/.config/dinamis_auth/) and on the signing endpoint.
"""


@click.group(help=CLI_DOCSTRING)
def app() -> None:
    """Click group for dinamis sdk subcommands."""


def _http(route: str):
    """Perform an HTTP request."""
    session = create_session()
    ret = session.get(
        f"{conn.endpoint}{route}",
        timeout=5,
        headers=conn.get_headers(),
    )
    ret.raise_for_status()
    return ret


def create_key() -> Dict[str, str]:
    return _http("create_api_key").json()


def list_keys() -> List[str]:
    return _http("list_api_keys").json()


def _revoke_key(key: str):
    _http(f"revoke_api_key?access_key={key}")
    log.info(f"API key {key} revoked")


@app.command(help="Create and show a new API key (not stored locally)")
def create():
    log.info(f"Got a new API key: {create_key()}")


@app.command(help="List all API keys on the signing endpoint")
def list():  # [redefined-builtin]
    log.info(f"All generated API keys: {list_keys()}")


@app.command(help="Revoke all API keys on the signing endpoint")
def revoke_all():
    keys = list_keys()
    for key in keys:
        _revoke_key(key)
    if not keys:
        log.info("No API key found.")


@app.command(help="Revoke an API key on the signing endpoint")
@click.argument("access_key")
def revoke(access_key: str):
    _revoke_key(access_key)


@app.command(help="Create and store locally an API key")
def register():
    ApiKeyStorage.from_config_dir(return_empty_if_not_present=True).add_key(
        ApiKey.from_dict(create_key())
    ).to_config_dir()
    log.info("API key successfully created and stored")


@app.command(help="Delete the stored API key")
@click.option("--dont-revoke", default=False)
def delete(dont_revoke: bool):
    if not dont_revoke:
        _revoke_key(
            ApiKeyStorage.from_config_dir(return_empty_if_not_present=True)
            .get_key_stored()
            .access_key
        )
    ApiKeyStorage.from_config_dir().remove_key().to_config_dir()
