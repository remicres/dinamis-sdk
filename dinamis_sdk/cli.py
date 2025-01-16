"""Dinamis Command Line Interface."""

from typing import Dict, List

import click

from .model import ApiKey
from .http import OAuth2ConnectionMethod
from .utils import get_logger_for, create_session

log = get_logger_for(__name__)
conn = OAuth2ConnectionMethod()


@click.group(help="Dinamis CLI")
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
    """Create an API key."""
    return _http("create_api_key").json()


def list_keys() -> List[str]:
    """List all generated API keys."""
    return _http("list_api_keys").json()


def revoke_key(key: str):
    """Revoke an API key."""
    _http(f"revoke_api_key?access_key={key}")
    log.info(f"API key {key} revoked")


@app.command(help="Create and show a new API key")
def create():
    """Create and show a new API key."""
    log.info(f"Got a new API key: {create_key()}")


@app.command(help="List all API keys")
def list():  # [redefined-builtin]
    """List all API keys."""
    log.info(f"All generated API keys: {list_keys()}")


@app.command(help="Revoke all API keys")
def revoke_all():
    """Revoke all API keys."""
    keys = list_keys()
    for key in keys:
        revoke_key(key)
    if not keys:
        log.info("No API key found.")


@app.command(help="Revoke an API key")
@click.argument("access_key")
def revoke(access_key: str):
    """Revoke an API key."""
    revoke_key(access_key)


@app.command(help="Get and store an API key")
def register():
    """Get and store an API key."""
    ApiKey.from_dict(create_key()).to_config_dir()
    log.info("API key successfully created and stored")


@app.command(help="Delete the stored API key")
@click.option("--dont-revoke", default=False)
def delete(dont_revoke: bool):
    """Delete the stored API key."""
    if not dont_revoke:
        revoke_key(ApiKey.from_config_dir().access_key)
    ApiKey.delete_from_config_dir()
