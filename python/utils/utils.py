import hashlib
import inspect
import os


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


def get_my_dirpath():
    """Return the /full/path/to/calling/script"""
    # based on https://stackoverflow.com/a/55469882
    # get the caller's stack frame and extract its file path
    frame_info = inspect.stack()[1]
    filepath = frame_info.filename
    # drop the reference to the stack frame to avoid reference cycles
    del frame_info

    # make the path absolute (optional)
    filepath = os.path.dirname(os.path.abspath(filepath))
    return filepath
