import click
from .utils import APIKEY_FILE, create_session, S3_SIGNING_ENDPOINT
from .auth import get_access_token
import os
import json
from typing import List, Dict


@click.group(help="Dinamis CLI")
def app() -> None:
    """Click group for dinamis sdk subcommands"""
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


def create_key() -> Dict[str, str]:
    """Create an API key."""
    return ret("create_api_key").json()


def list_keys() -> List[str]:
    """List all generated API keys."""
    return ret("list_api_keys").json()


def revoke_key(key: str):
    """Revoke an API key."""
    ret(f"revoke_api_key?key={key}")
    print(f"API key {key} revoked")


@app.command(help="Create and show a new API key")
def create():
    print(f"Got a new API key: {create_key()}")


@app.command(help="List all API keys")
def list():
    print(f"All generated API keys: {list_keys()}")


@app.command(help="Revoke all API keys")
def revoke_all():
    keys = list_keys()
    for key in keys:
        revoke_key(key)
    if not keys:
        print("No API key found.")


@app.command(help="Revoke an API key")
@click.option(
    "--key",
    prompt="Please enter the access key to revoke",
    help="Access key to revoke",
)
def revoke(key: str):
    revoke_key(key)


@app.command(help="Get and store an API key")
def register():
    with open(APIKEY_FILE, 'w') as f:
        json.dump(create_key(), f)
    print(f"API key successfully created and stored in {APIKEY_FILE}")


@app.command(help="Delete the stored API key")
def delete():
    if os.path.isfile(APIKEY_FILE):
        os.remove(APIKEY_FILE)
        print(f"File {APIKEY_FILE} deleted!")
    else:
        print("No API key stored!")
