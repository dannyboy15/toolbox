from base64 import b64encode
import civis
import click
import json


# test credential
# CIVIS_CREDENTIAL_ID = 20413


# creates a group of subcommands
@click.group()
def cli():
    pass


@cli.command()
@click.argument("cred_id")
@click.argument("path")
def update(cred_id, path):
    """Update a credential in Civis.

    `Args:`
        path: str
            Path to a json file with the updated credentials.
    """
    try:
        with open(path) as fd:
            data = json.load(fd)
    except Exception as e:
        raise RuntimeError(f"Error reading the file: {e}")

    username = f"{len(data)}-partners"
    password = b64encode(json.dumps(data).encode("utf-8"))
    description = ", ".join(data)

    client = civis.APIClient()
    client.credentials.put(
        cred_id,
        "Custom",
        username,
        password,
        description=description)


@cli.command()
@click.argument("cred_id")
@click.option("-u", "--user")
@click.option("-p", "--permission")
def share(cred_id, user, permission="read"):
    """Share a credential in Civis.

    `Args:`
        path: str
            Path to a json file with the updated credentials.
    """
    users = user.split(",")
    client = civis.APIClient()
    client.credentials.put_shares_users(
        cred_id,
        users,
        permission
    )


@cli.command()
@click.argument("cred_id")
@click.option("-v", "--verbose", is_flag=True)
def describe(cred_id, verbose):
    """

    """
    client = civis.APIClient()
    cred = client.credentials.get(cred_id)
    shares = client.credentials.list_shares(cred_id)

    if verbose:
        cred["shares"] = shares
        print(json.dumps(cred, indent=2))
    else:
        print(cred["name"])


if __name__ == "__main__":
    cli()
