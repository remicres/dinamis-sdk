"""Dinamis Command Line Interface."""
import click
from .utils import APIKEY_FILE, create_session, S3_SIGNING_ENDPOINT, log
from .auth import get_access_token
import os
import json
from typing import List, Dict


@click.group(help="Dinamis CLI")
def app() -> None:
    """Click group for dinamis sdk subcommands."""
    pass


def http(route: str):
    """Perform an HTTP request."""
    session = create_session()
    ret = session.get(
        f"{S3_SIGNING_ENDPOINT}{route}",
        timeout=5,
        headers={"authorization": f"bearer {get_access_token()}"}
    )
    ret.raise_for_status()
    return ret


def create_key() -> Dict[str, str]:
    """Create an API key."""
    return http("create_api_key").json()


def list_keys() -> List[str]:
    """List all generated API keys."""
    return http("list_api_keys").json()


def revoke_key(key: str):
    """Revoke an API key."""
    http(f"revoke_api_key?access_key={key}")
    log.info(f"API key {key} revoked")


@app.command(help="Create and show a new API key")
def create():
    """Create and show a new API key."""
    log.info(f"Got a new API key: {create_key()}")


@app.command(help="List all API keys")
def list():
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
    with open(APIKEY_FILE, 'w') as f:
        json.dump(create_key(), f)
    log.info(f"API key successfully created and stored in {APIKEY_FILE}")


@app.command(help="Delete the stored API key")
@click.option("--dont-revoke", default=False)
def delete(dont_revoke):
    """Delete the stored API key."""
    if os.path.isfile(APIKEY_FILE):
        if not dont_revoke:
            with open(APIKEY_FILE, encoding='UTF-8') as json_file:
                api_key = json.load(json_file)
                if "access-key" in api_key:
                    revoke_key(api_key["access-key"])
        os.remove(APIKEY_FILE)
        log.info(f"File {APIKEY_FILE} deleted!")
    else:
        log.info("No API key stored!")
