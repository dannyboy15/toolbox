import os
import requests


def create_one_time_secret(secret, url_password=None, expires_in=600,
                           recipient=None, ots_username=None,
                           ots_password=None):
    """Create a onetime secret url.

    This is based on `OneTimeSecret API <https://onetimesecret.com/>`_.

    `Args:`
        secret: str
            The data to include in the one time secret.
        url_password: str
            The password to require in the one time secret.
        expires_in: int
            The number of seconds before the secret expires. Defaults to 600.
        recipient: str
            The email address to send the url to.
        ots_username: str
            The username for access to the one time secret api.
        ots_password: str
            The password for access to the one time secret api.
    `Returns:`
        str
            The url for the secret.
    """
    base_url = "https://onetimesecret.com/api/v1"
    args = {
        "secret": secret,
        "passphrase": url_password,
        "ttl": expires_in,
        "recipient": recipient,
    }

    ots_username = ots_username or os.environ["OTS_USERNAME"]
    ots_password = ots_password or os.environ["OTS_PASSWORD"]

    resp = requests.post(
        f"{base_url}/share", params=args, auth=(ots_username, ots_password))
    data = resp.json()
    secret_url = (f"{base_url.replace('/api/v1', '')}/"
                  f"secret/{data['secret_key']}")

    return secret_url
