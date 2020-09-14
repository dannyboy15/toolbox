import hashlib


def md5_hash(string):
    """Return the md5 hash of a string.

    `Args:`
        string: str
            The string to hash
    `Returns:`
        str
            The hashed string.
    """
    return hashlib.md5(string.encode("utf-8")).hexdigest()
