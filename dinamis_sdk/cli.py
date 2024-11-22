import click
from .utils import APIKEY_FILE, create_session, S3_SIGNING_ENDPOINT
from .auth import get_access_token
import os
import json


@click.group(help="Dinamis CLI")
def app() -> None:
    """Click group for dinamis sdk subcommands"""
    pass


def create_key() -> dict:
    """
    Create an API key
    """
    session = create_session()
    ret = session.get(
        f"{S3_SIGNING_ENDPOINT}create_api_key",
        timeout=5,
        headers={"authorization": f"bearer {get_access_token()}"}
    )
    ret.raise_for_status()
    return ret.json()


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
